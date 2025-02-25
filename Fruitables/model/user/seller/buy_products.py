from flask import Flask, render_template, redirect, url_for, request, flash, session
import os
from db import mysql

app = Flask(__name__)

# SHOW CATEGORY
def model_show_category():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM tbl_category")
  categories = cur.fetchall()
  cur.close()
  return categories

# SHOW PRODUCTS
# def model_show_product(id_user):
#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT tbl_product.*, tbl_category.category_name
#         FROM tbl_product
#         JOIN tbl_category ON tbl_product.id_category = tbl_category.id_category
#         WHERE tbl_product.status = 'listed' AND tbl_product.id_user != %s
#         ORDER BY tbl_product.id_product ASC
#     """, (id_user,))
#     products = cur.fetchall()
#     cur.close()
#     return products

# SHOW PRODUCTS
def model_show_product(id_user):
    print(f"Logged in user ID: {id_user}")  # Debugging
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT tbl_product.*, tbl_category.category_name
        FROM tbl_product
        JOIN tbl_category ON tbl_product.id_category = tbl_category.id_category
        WHERE tbl_product.status = 'listed' AND tbl_product.id_user != %s
        ORDER BY tbl_product.id_product ASC
    """, (id_user,))
    products = cur.fetchall()
    cur.close()
    return products


# SHOW FRUITS
def model_show_fruits():
  cur = mysql.connection.cursor()
  cur.execute("""
    SELECT tbl_product.*, tbl_category.category_name
    FROM tbl_product
    JOIN tbl_category ON tbl_product.id_category = tbl_category.id_category
    WHERE tbl_product.status = 'listed' AND tbl_category.category_name = 'Fruits'
    ORDER BY tbl_product.id_product ASC;
  """)
  fruits = cur.fetchall()
  cur.close()
  return fruits

# SHOW VEGETABLES
def model_show_vegetables():
  cur = mysql.connection.cursor()
  cur.execute("""
    SELECT tbl_product.*, tbl_category.category_name
    FROM tbl_product
    JOIN tbl_category ON tbl_product.id_category = tbl_category.id_category
    WHERE tbl_product.status = 'listed' AND tbl_category.category_name = 'Vegetables'
    ORDER BY tbl_product.id_product ASC;
  """)
  vegetables = cur.fetchall()
  cur.close()
  return vegetables

# PRODUCT DETAILS
def model_product_detail(id_product):
  cur = mysql.connection.cursor()
  cur.execute("""
      SELECT p.id_product, p.image, p.product_name, p.product_price, p.description, c.category_name
      FROM tbl_product p
      JOIN tbl_category c ON p.id_category = c.id_category WHERE p.id_product = %s;
  """, (id_product,))
  product_detail = cur.fetchone()
  cur.close()
  if product_detail is None:
      return None
  return product_detail

