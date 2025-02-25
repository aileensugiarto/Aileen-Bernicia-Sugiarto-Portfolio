from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from db import mysql
from datetime import datetime

app = Flask(__name__)

# CART
def model_cart_seller(id_user):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT a.id_cart, a.qty, c.* FROM tbl_cart a JOIN tbl_user b ON a.id_user = b.id_user
                JOIN tbl_product c ON a.id_product = c.id_product WHERE a.id_user = %s""", (id_user,))
    data = cur.fetchall()
    cur.execute("SELECT SUM(price) FROM tbl_cart WHERE id_user = %s", (id_user,))
    total = cur.fetchone()[0]
    return render_template('user/seller/buy_products/cart.html', data_cart=data, total_price=total)

# ADD TO CART
def model_add_cart_seller():
    if request.method == "POST":
        id_user = request.form['form_id_user']
        id_product = request.form['form_id_product']
        price = request.form['form_price']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_cart VALUES (%s, %s, %s, %s, %s)", ('', id_user, id_product, 1, price))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('cart_seller', id_user=id_user))
    return render_template('user/seller/index.html')

# UPDATE CART
def model_update_cart_seller():
    id_cart = request.form['form_id_cart']
    id_product = request.form['form_id_product']
    price = request.form['form_price']
    qty = request.form['form_qty']
    id_user = request.form['form_id_user']

    cur = mysql.connection.cursor()

    if 'plus' in request.form:
        qty_new = int(qty) + 1
        price_new = qty_new * int(price)
        cur.execute("UPDATE tbl_cart SET price = %s, qty = %s WHERE id_cart = %s", (price_new, qty_new, id_cart))
    else:
        if int(qty) == 1:
            return redirect(url_for('cart_seller', id_user=id_user))
        else:
            qty_new = int(qty) - 1
            price_new = qty_new * int(price)
            cur.execute("UPDATE tbl_cart SET price = %s, qty = %s WHERE id_cart = %s", (price_new, qty_new, id_cart))

    mysql.connection.commit()
    return redirect(url_for('cart_seller', id_user=id_user))

# DELETE CART
def model_delete_cart_seller(id_cart):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tbl_cart WHERE id_cart = %s", (id_cart,))
    mysql.connection.commit()
    cur.close()

    # flash("Item Successfully Deleted", "danger")
    return redirect(url_for('cart_seller', id_user=session['id_user']))

