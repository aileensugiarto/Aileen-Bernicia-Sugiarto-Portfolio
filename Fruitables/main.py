from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
import os, requests
from db import mysql
from flask_mysqldb import MySQL
from datetime import datetime
import webbrowser

# Admin
from model.admin.auth import model_login, model_logout
from model.admin.user import model_user, model_add_user, model_edit_user, model_delete_user, model_process_edit_user
from model.admin.transaction import model_transaction, model_process_delivery, model_detail_transaction, model_process_sent
from model.admin.payment import model_payment
from model.admin.earnings import admin_earnings

# User
from model.user.auth import model_register_user, model_login_user, model_logout_user

# SELLER
# Product
from model.user.seller.product import model_product, model_add_product, model_edit_product, model_process_edit_product, model_delete_product, move_sent_to_unlisted_product
# Category
from model.user.seller.category import model_category, model_add_category, model_edit_category, model_process_edit_category, model_delete_category
# Sales
from model.user.seller.sales import model_sales_report
# Buy Products
from model.user.seller.buy_products import model_show_category, model_show_product, model_show_fruits, model_show_vegetables, model_product_detail
# Profile
from model.user.seller.profile import model_profile_seller, model_edit_profile_seller, model_process_edit_profile_seller
# Add to Cart
from model.user.seller.cart import model_cart_seller, model_add_cart_seller, model_update_cart_seller, model_delete_cart_seller
# Checkout
from model.user.seller.checkout import get_provinces_seller, get_seller_address, model_seller_checkout, model_seller_process_checkout
# Order
from model.user.seller.order import model_order_seller, model_billing_seller, model_save_payment_info_seller, model_process_sent_seller

# BUYER
# Product
from model.user.buyer.product import model_show_category, model_show_product, model_show_fruits, model_show_vegetables, model_product_detail
# Cart
from model.user.buyer.cart import model_cart, model_add_cart, model_update_cart, model_delete_cart
# Checkout
from model.user.buyer.checkout import model_checkout, model_process_checkout, get_provinces
# Order
from model.user.buyer.order import model_order, model_billing, model_save_payment_info
# Review
from model.user.buyer.review import model_reviews, model_add_review
# Profile
from model.user.buyer.profile import model_profile, model_edit_profile, model_process_edit_profile
# Search
from model.user.buyer.search_results import model_search_results

app = Flask(__name__)

app.secret_key = 'aileen'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fruitables'
app.config['MYSQL_PORT'] = 3306
app.config['UPLOAD_FOLDER'] = 'static/uploads'

mysql.init_app(app)

RAJAONGKIR_API_KEY = '71bd102318358b6da806fe670361d8e3'
RAJAONGKIR_BASE_URL = 'https://api.rajaongkir.com/starter/'
ORIGIN_CITY_ID = '444'


# REGISTER USER
@app.route('/register', methods=['GET', 'POST'])
def register():
  return model_register_user()

# LOGIN USER
@app.route('/login', methods=['GET', 'POST'])
def login():
  return model_login_user()

# LOGOUT USER
@app.route('/logout')
def logout():
  return model_logout_user()



# ADMIN
# Routing to LOGIN ADMIN
@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
  return model_login()

# Routing to LOGOUT ADMIN
@app.route('/logout_admin')
def logout_admin():
  return model_logout()


# Rouing to DASHBOARD
@app.route('/dashboard')
def dashboard():
  if "loggedin" in session:
    cur = mysql.connection.cursor()

    # Total Users
    cur.execute("SELECT COUNT(id_user) FROM tbl_user")
    data_user = cur.fetchone()[0]

    # Total Transactions
    cur.execute("SELECT COUNT(id_transaction) FROM tbl_payment_transaction")
    data_transaction = cur.fetchone()[0]

    # Total Payment
    cur.execute("SELECT COUNT(id_payment) FROM tbl_payment")
    data_payment = cur.fetchone()[0]

    cur.close()

    return render_template('admin/admin_dashboard.html', total_user=data_user, total_transaction=data_transaction, total_payment=data_payment)

  flash('Please Login.', 'danger')
  return redirect(url_for('login_admin'))


# USER
@app.route('/user')
def user():
  return model_user()

# ADD USER
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
  return model_add_user()

# EDIT USER
@app.route('/edit_user/<int:id>', methods=['GET'])
def edit_user(id):
  return model_edit_user(id)

# PROCESS EDIT USER
@app.route('/process_edit_user', methods=['POST'])
def process_edit_user():
  return model_process_edit_user()

# DELETE USER
@app.route('/delete_user/<int:id>', methods=['GET'])
def delete_user(id):
  return model_delete_user(id)


# SALES TRANSACTION
@app.route('/transaction')
def transaction():
  return model_transaction()

# DETAIL TRANSACTION
@app.route('/detail_transaction/<int:id_transaction>', methods=['GET'])
def detail_transaction(id_transaction):
    return model_detail_transaction(id_transaction)

# PROCESS DELIVERY
@app.route('/process_delivery', methods=['POST'])
def process_delivery():
    return model_process_delivery()

# PROCESS SENT
@app.route('/process_sent', methods=['POST'])
def process_sent():
  return model_process_sent()

# PAYMENT
@app.route('/payment')
def payment():
  return model_payment()


# EARNINGS
@app.route('/earnings')
def earnings():
  return admin_earnings()
# ADMIN END



# BUYER START

# BUYER HOME PAGE
@app.route('/buyer_home')
def buyer_home():
    return render_template('user/buyer/index.html')


# SEARCH RESULTS
@app.route('/search_results', methods=['GET'])
def search_results():
    return model_search_results()


# ABOUT US
@app.route('/about_us')
def about_us():
  return render_template('user/buyer/about_us.html')


# Routing to SHOP ALL
@app.route('/shop_all')
def shop_all():
  data_category = model_show_category()
  data_product = model_show_product()
  return render_template('user/buyer/shop_all.html', category=data_category, product=data_product)

# Routing to SHOP FRUITS
@app.route('/shop_fruits')
def shop_fruits():
  data_fruit = model_show_fruits()
  return render_template('user/buyer/shop_fruits.html', fruit=data_fruit)

# Routing to SHOP VEGETABLES
@app.route('/shop_vegetables')
def shop_vegetables():
  data_vegetable = model_show_vegetables()
  return render_template('user/buyer/shop_vegetables.html', vegetable=data_vegetable)

# PRODUCT DETAIL
@app.route('/product_detail/<int:id_product>', methods=['GET'])
def product_detail(id_product):
    product_detail = model_product_detail(id_product)
    if product:
        return render_template('user/buyer/product_detail.html', product_detail=product_detail)
    else:
        return "Product not found", 404


# ADD TO CART
@app.route('/add_cart', methods=['GET', 'POST'])
def add_cart():
  return model_add_cart()

# CART
@app.route('/cart/<int:id_user>', methods=['GET', 'POST'])
def cart(id_user):
  return model_cart(id_user)

# UPDATE CART
@app.route('/update_cart', methods=['GET', 'POST'])
def update_cart():
  return model_update_cart()

# DELETE CART
@app.route('/delete_cart/<int:id_cart>', methods=['GET'])
def delete_cart(id_cart):
  return model_delete_cart(id_cart)


# CITIES
@app.route('/get_cities/<id_province>', methods=['GET'])
def cities(id_province):
  url = f"{RAJAONGKIR_BASE_URL}city?province={id_province}"
  headers = {'key': RAJAONGKIR_API_KEY}
  response = requests.get(url, headers=headers)
  data = response.json()
  if 'rajaongkir' in data and 'results' in data['rajaongkir']:
    return jsonify(data['rajaongkir']['results'])
  else:
    return jsonify({'error': 'Unable to fetch cities', 'details': data})

# CHECKOUT
@app.route('/checkout/<int:id_user>', methods=['GET', 'POST'])
def checkout(id_user):
  return model_checkout(id_user)

# PROCESS CHECKOUT
@app.route('/process_checkout', methods=['GET', 'POST'])
def process_checkout():
  return model_process_checkout()


# Routing to ORDER
@app.route('/order/<int:id_user>', methods=['GET'])
def order(id_user):
  return model_order(id_user)

# BILLING
@app.route('/billing', methods=['GET', 'POST'])
def billing():
  return model_billing()

# SAVE PAYMENT INFO
@app.route('/save_payment_info', methods=['POST'])
def save_payment_info():
  return model_save_payment_info()

# # PROCESS SENT
# @app.route('/sent', methods=['POST'])
# def process_sent():
#   return model_process_sent()


# REVIEW
@app.route('/reviews', methods=['GET'])
def reviews():
  return model_reviews()

# WRITE/ADD A REVIEW
@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
  return model_add_review()


# Routing to PROFILE
@app.route('/profile')
def profile():
  if "loggedin" in session:
    user_id = session['id_user']  # Get the logged-in user's ID
    cur = mysql.connection.cursor()

    # Get user profile data along with the count of bought products
    cur.execute("""
        SELECT u.id_user, u.name, u.username, u.telp, u.address, u.email, u.role, p.bio, p.profile_picture,
        COUNT(pt.id_transaction) AS total_bought_products
        FROM tbl_user u
        LEFT JOIN tbl_profile p ON u.id_user = p.id_user
        LEFT JOIN tbl_payment_transaction pt ON u.id_user = pt.id_user
        WHERE u.id_user = %s AND pt.order_status IN ('packaging', 'delivery', 'sent')
        GROUP BY u.id_user, p.bio, p.profile_picture
    """, (user_id,))

    data_profile = cur.fetchall()
    cur.close()

    # Pass both the profile data and total bought products to the template
    return render_template(
        'user/buyer/profile.html',
        data_profile=data_profile,
    )

  flash('Please Login', 'danger')
  return redirect(url_for('login'))


# EDIT PROFILE
@app.route('/edit_profile/<int:id>', methods=['GET'])
def edit_profile(id):
  return model_edit_profile(id)

# PROCESS EDIT PROFILE
@app.route('/process_edit_profile', methods=['POST'])
def process_edit_profile():
  return model_process_edit_profile()
# BUYER END



# SELLER START

# SELLER HOME PAGE
@app.route('/seller_home')
def seller_home():
  if "loggedin" in session:
    user_id = session['id_user']
    cur = mysql.connection.cursor()

    # Total Products
    cur.execute("""
      SELECT COUNT(id_product)
      FROM tbl_product
      WHERE id_user = %s
    """, (user_id,))
    data_product = cur.fetchone()[0]

    # Total Sales
    cur.execute("""
      SELECT SUM(pt.total_price)
      FROM tbl_payment_transaction pt
      JOIN tbl_payment_transaction_detail ptd ON pt.id_transaction = ptd.id_transaction
      JOIN tbl_product p ON p.id_product = ptd.id_product
      WHERE p.id_user = %s AND pt.order_status IN ('packaging', 'delivery', 'sent')
    """, (user_id,))
    total_sales = cur.fetchone()[0] or 0  # Use 0 if there are no sales

    # Best-Selling Product
    cur.execute("""
      SELECT p.product_name, SUM(ptd.qty) AS total_qty
      FROM tbl_payment_transaction pt
      JOIN tbl_payment_transaction_detail ptd ON pt.id_transaction = ptd.id_transaction
      JOIN tbl_product p ON p.id_product = ptd.id_product
      WHERE p.id_user = %s AND pt.order_status IN ('packaging', 'delivery', 'sent')
      GROUP BY p.id_product, p.product_name
      ORDER BY total_qty DESC
      LIMIT 1
    """, (user_id,))
    best_selling_product_data = cur.fetchone()
    if best_selling_product_data:
      best_selling_product = best_selling_product_data[0]  # Product name
      best_selling_qty = best_selling_product_data[1]      # Total quantity sold
    else:
      best_selling_product = "No sales"
      best_selling_qty = 0

    return render_template(
      'user/seller/index.html', total_product=data_product, total_sales=total_sales, best_selling_product=best_selling_product)

  flash('Please Login.', 'danger')
  return redirect(url_for('login'))

# Routing to PRODUCT
@app.route('/product', methods=['GET', 'POST'])
def product():
  return model_product()

# ADD PRODUCT
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
  return model_add_product()

#EDIT PRODUCT
@app.route('/edit_product/<int:id>', methods=['GET'])
def edit_product(id):
  return model_edit_product(id)

# PROCESS EDIT PRODUCT
@app.route('/process_edit_product', methods=['POST'])
def process_edit_product():
  return model_process_edit_product()

# DELETE PRODUCT
@app.route('/delete_product/<int:id>', methods=['GET'])
def delete_product(id):
  return model_delete_product(id)


# Routing to CATEGORY
@app.route('/category')
def category():
    return model_category()

# ADD CATEGORY
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    return model_add_category()

# EDIT CATEGORY
@app.route('/edit_category/<int:id>', methods=['GET'])
def edit_category(id):
    return model_edit_category(id)

# PROCESS EDIT CATEGORY
@app.route('/process_edit_category', methods=['POST'])
def process_edit_category():
    return model_process_edit_category()

# DELETE CATEGORY
@app.route('/delete_category/<int:id>', methods=['GET'])
def delete_category(id):
    return model_delete_category(id)


# Routing to SALES
@app.route('/sales_report')
def sales_report():
  return model_sales_report()


# Routing to BUY PRODUCTS
@app.route('/buy_products')
def buy_products():
  data_category = model_show_category()
  data_product = model_show_product()
  return render_template('user/seller/buy_products/buy_products.html', category=data_category, product=data_product)


# ADD TO CART SELLER
@app.route('/add_cart_seller', methods=['GET', 'POST'])
def add_cart_seller():
    return model_add_cart_seller()

# CART
@app.route('/cart_seller/<int:id_user>', methods=['GET', 'POST'])
def cart_seller(id_user):
    return model_cart_seller(id_user)

# UPDATE CART
@app.route('/update_cart_seller', methods=['GET', 'POST'])
def update_cart_seller():
    return model_update_cart_seller()

# DELETE CART
@app.route('/delete_cart_seller/<int:id_cart>', methods=['GET'])
def delete_cart_seller(id_cart):
    return model_delete_cart_seller(id_cart)


# CITIES (SELLER)
@app.route('/get_cities_seller/<id_province>', methods=['GET'])
def get_cities_seller(id_province):
    url = f"{RAJAONGKIR_BASE_URL}city?province={id_province}"
    headers = {'key': RAJAONGKIR_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'rajaongkir' in data and 'results' in data['rajaongkir']:
        return jsonify(data['rajaongkir']['results'])
    else:
        return jsonify({'error': 'Unable to fetch cities', 'details': data})

# CHECKOUT (SELLER)
@app.route('/checkout_seller/<int:id_user>', methods=['GET', 'POST'])
def checkout_seller(id_user):
    return model_seller_checkout(id_user)

# PROCESS CHECKOUT (SELLER)
@app.route('/process_checkout_seller', methods=['POST'])
def process_checkout_seller():
    return model_seller_process_checkout()


# Routing to ORDER SELLER
@app.route('/order_seller/<int:id_user>', methods=['GET'])
def order_seller(id_user):
  return model_order_seller(id_user)

# BILLING SELLER
@app.route('/billing_seller', methods=['GET', 'POST'])
def billing_seller():
  return model_billing_seller()

# SAVE PAYMENT INFO SELLER
@app.route('/save_payment_info', methods=['POST'])
def save_payment_info_seller():
  return model_save_payment_info_seller()

# PROCESS SENT SELLER
@app.route('/sent_seller', methods=['POST'])
def process_sent_seller():
  return model_process_sent_seller()


@app.route('/move_sent_to_product')
def move_sent_to_product_route():
    return move_sent_to_unlisted_product()


# Routing to PROFILE
@app.route('/profile_seller')
def profile_seller():
    if "loggedin" in session:
        user_id = session['id_user']  # Get the logged-in user's ID
        cur = mysql.connection.cursor()

        # Query to get the total number of products for the current seller
        cur.execute("""
            SELECT COUNT(id_product)
            FROM tbl_product
            WHERE id_user = %s
        """, (user_id,))
        total_products = cur.fetchone()[0]

        # Total Sales
        cur.execute("""
            SELECT SUM(pt.total_price)
            FROM tbl_payment_transaction pt
            JOIN tbl_payment_transaction_detail ptd ON pt.id_transaction = ptd.id_transaction
            JOIN tbl_product p ON p.id_product = ptd.id_product
            WHERE p.id_user = %s AND pt.order_status IN ('packaging', 'delivery', 'sent')
        """, (user_id,))
        total_sales = cur.fetchone()[0] or 0  # Use 0 if no sales

        # Best-Selling Product
        cur.execute("""
            SELECT p.product_name, SUM(ptd.qty) AS total_qty
            FROM tbl_payment_transaction pt
            JOIN tbl_payment_transaction_detail ptd ON pt.id_transaction = ptd.id_transaction
            JOIN tbl_product p ON p.id_product = ptd.id_product
            WHERE p.id_user = %s AND pt.order_status IN ('packaging', 'delivery', 'sent')
            GROUP BY p.id_product, p.product_name
            ORDER BY total_qty DESC
            LIMIT 1
        """, (user_id,))
        best_selling_product_data = cur.fetchone()
        if best_selling_product_data:
            best_selling_product = best_selling_product_data[0]  # Product name
            best_selling_qty = best_selling_product_data[1]      # Total quantity sold
        else:
            best_selling_product = "No sales"
            best_selling_qty = 0

        # Get user profile data
        cur.execute("""
            SELECT u.id_user, u.name, u.username, u.telp, u.address, u.email, u.role, p.bio, p.profile_picture
            FROM tbl_user u
            LEFT JOIN tbl_profile p ON u.id_user = p.id_user
            WHERE u.id_user = %s
        """, (user_id,))
        data_profile_seller = cur.fetchall()

        cur.close()

        # Pass both the profile data, total products count, total sales, and best-selling product to the template
        return render_template(
            'user/profile/profile.html',
            data_profile_seller=data_profile_seller,
            total_products=total_products,
            total_sales=total_sales,
            best_selling_product=best_selling_product,
            best_selling_qty=best_selling_qty
        )

    flash('Please Login', 'danger')
    return redirect(url_for('login'))


# EDIT PROFILE
@app.route('/edit_profile_seller/<int:id>', methods=['GET'])
def edit_profile_seller(id):
  return model_edit_profile_seller(id)

# PROCESS EDIT PROFILE
@app.route('/process_edit_profile_seller', methods=['POST'])
def process_edit_profile_seller():
  return model_process_edit_profile_seller()


# SELLER END


if __name__ == '__main__':
  webbrowser.open("http://127.0.0.1:5000/login")
  app.run(debug=True)