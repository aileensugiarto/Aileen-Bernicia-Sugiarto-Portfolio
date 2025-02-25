from flask import Flask, render_template, redirect, url_for, request, session
from db import mysql
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = 'aileen'

# Rajaongkir for shipping
RAJAONGKIR_API_KEY = '71bd102318358b6da806fe670361d8e3'
RAJAONGKIR_BASE_URL = 'https://api.rajaongkir.com/starter/'

# GET PROVINCES
def get_provinces():
  url = f"{RAJAONGKIR_BASE_URL}province"
  headers = {'key': RAJAONGKIR_API_KEY}
  response = requests.get(url, headers=headers)
  data = response.json()
  if 'rajaongkir' in data and 'results' in data['rajaongkir']:
    return data['rajaongkir']['results']
  else:
    print(f"Error fetching provinces: {data}")
    return []

# GET USER ADDRESS FROM tbl_user
def get_user_address(id_user):
  cur = mysql.connection.cursor()
  cur.execute("SELECT address FROM tbl_user WHERE id_user = %s", (id_user,))
  address = cur.fetchone()
  cur.close()
  return address[0] if address else ""

# CHECKOUT
def model_checkout(id_user):
  cur = mysql.connection.cursor()
  cur.execute("""
    SELECT a.id_cart, a.qty, c.*
    FROM tbl_cart a
    JOIN tbl_user b ON a.id_user = b.id_user
    JOIN tbl_product c ON a.id_product = c.id_product
    WHERE a.id_user = %s
  """, (id_user,))
  data = cur.fetchall()

  # Updated to correctly sum the total price (quantity * price)
  cur.execute("""
    SELECT SUM(a.qty * c.product_price)
    FROM tbl_cart a
    JOIN tbl_product c ON a.id_product = c.id_product
    WHERE a.id_user = %s
  """, (id_user,))
  total = cur.fetchone()[0]

  provinces = get_provinces()
  user_address = get_user_address(id_user)  # Fetch address from tbl_user
  return render_template('user/buyer/checkout.html', data_cart=data, total_price=total,
                        provinces=provinces, user_address=user_address)


# PROCESS CHECKOUT
def model_process_checkout():
  id_user = request.form['form_id_user']
  total_price = request.form['final_total_price']
  information = request.form['form_information']
  transaction_date = datetime.now().strftime("%Y-%m-%d")
  province = request.form['province']
  city = request.form['city']

  # Insert payment transaction (remove 'courier' field)
  cur = mysql.connection.cursor()
  cur.execute("""
      INSERT INTO tbl_payment_transaction
      (id_transaction, id_user, information, order_status, transaction_date, total_price, province, city) 
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
  """, ('', id_user, information, 'billing', transaction_date, total_price, province, city))

  mysql.connection.commit()

  id_transaction = cur.lastrowid
  id_products = request.form.getlist('form_id_product[]')
  id_qty = request.form.getlist('form_qty[]')
  id_price = request.form.getlist('form_price[]')

  # Loop through each product in the checkout and update stock
  for product, qty, price in zip(id_products, id_qty, id_price):
    # Insert into transaction details
    cur.execute("""
      INSERT INTO tbl_payment_transaction_detail
      (id_detail_transaction, id_transaction, id_product, qty, price)
      VALUES (%s, %s, %s, %s, %s)
    """, ('', id_transaction, product, qty, price))

    # Decrease the stock of the product
    cur.execute("""
      UPDATE tbl_product
      SET product_stock = product_stock - %s
      WHERE id_product = %s
    """, (qty, product))
  mysql.connection.commit()

  # Clear cart after checkout
  id_carts = request.form.getlist('form_id_cart[]')
  for id_cart in id_carts:
    cur.execute("DELETE FROM tbl_cart WHERE id_cart = %s", (id_cart,))

  mysql.connection.commit()
  cur.close()

  return redirect(url_for('order', id_user=session['id_user']))
