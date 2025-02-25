from flask import Flask, render_template, redirect, url_for, request, flash
from db import mysql

app = Flask(__name__)

# SEARCH PRODUCTS ONLY
def model_search_results():
    query = request.args.get('query')
    if query:
        # Fetch the matching products from the database
        cur = mysql.connection.cursor()
        cur.execute("""
          SELECT tbl_product.*, tbl_category.category_name
          FROM tbl_product
          JOIN tbl_category ON tbl_product.id_category = tbl_category.id_category
          WHERE tbl_product.status = 'listed' AND tbl_product.product_name LIKE %s
      """, ('%' + query + '%',))

        products = cur.fetchall()
        cur.close()

        # Pass the products and the search query to the template
        return render_template('user/buyer/search_results.html', query=query, products=products)
    else:
        flash('No search query provided', 'warning')
        return redirect(url_for('shop_all'))