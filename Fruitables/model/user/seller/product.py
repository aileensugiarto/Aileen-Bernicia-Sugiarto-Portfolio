from flask import Flask, render_template, redirect, url_for, request, flash
import os
from db import mysql
from flask import session


app = Flask(__name__)

app.secret_key = 'aileen'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Get CATEGORY
def get_category():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_category")
    categories = cur.fetchall()
    cur.close()
    return categories

# PRODUCT
def model_product():
    # Check if user is logged in
    if "loggedin" in session:
        id_user = session['id_user']
    else:
        flash("You must be logged in to view products.", "danger")
        return redirect(url_for('login'))

    # Query to fetch products belonging to the logged-in user, including both 'listed' and 'unlisted'
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT tbl_product.*, tbl_category.category_name
        FROM tbl_product
        JOIN tbl_category ON tbl_product.id_category = tbl_category.id_category
        WHERE tbl_product.id_user = %s
        AND tbl_product.status IN ('listed', 'unlisted')
        ORDER BY tbl_product.id_product ASC
    """, (id_user,))
    data = cur.fetchall()
    cur.close()

    # Render the products page, passing the data for the products
    return render_template('user/seller/product/product.html', data_product=data)

# ADD PRODUCT
def model_add_product():
    if request.method == "POST":
        product_name = request.form['form_product_name']
        id_category = request.form['form_id_category']
        price = request.form['form_price']
        description = request.form['form_description']
        product_stock = request.form['form_product_stock']
        status = request.form['form_status']

        if "loggedin" in session:
            id_user = session['id_user']  # Get the current logged-in user's ID
        else:
            flash("You must be logged in to add a product.", "danger")
            return redirect(url_for('login'))

        file = request.files['form_image']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cur = mysql.connection.cursor()
        cur.execute(
            """
            INSERT INTO tbl_product (product_name, id_category, product_price, description, product_stock, image, id_user, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (product_name, id_category, price, description, product_stock, filename, id_user, status)
        )
        mysql.connection.commit()
        cur.close()

        flash("Product added successfully!", "success")
        return redirect(url_for('product'))

    return render_template('user/seller/product/add_product.html', category=get_category())


# EDIT PRODUCT
def model_edit_product(id):
    if "loggedin" in session:
        id_user = session['id_user']
    else:
        flash("You must be logged in to edit a product.", "danger")
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_product WHERE id_product = %s AND id_user = %s", (id, id_user))
    data = cur.fetchone()

    if data:
        return render_template('user/seller/product/edit_product.html', data_product=data, category=get_category())
    else:
        flash("You don't have permission to edit this product.", "danger")
        return redirect(url_for('product'))

# PROCESS EDIT PRODUCT
def model_process_edit_product():
    if "loggedin" in session:
        id_user = session['id_user']
    else:
        flash("You must be logged in to edit a product.", "danger")
        return redirect(url_for('login'))

    product_name = request.form['form_product_name']
    price = request.form['form_price']
    description = request.form['form_description']
    product_stock = request.form['form_product_stock']
    id_product = request.form['form_id_product']
    id_category = request.form['form_id_category']
    status = request.form['form_status']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_product WHERE id_product = %s AND id_user = %s", (id_product, id_user))
    data = cur.fetchone()

    if data:
        cur.execute("UPDATE tbl_product SET product_name = %s, id_category = %s, description = %s, product_price = %s, product_stock = %s, status = %s WHERE id_product = %s",
                    (product_name, id_category, description, price, product_stock, status, id_product))
        mysql.connection.commit()

        file = request.files['form_image']
        filename = file.filename

        if file and filename != '':
            # Create a unique filename for the new image to avoid overwriting the old one
            new_filename = f"{id_product}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

            # Update the product record with the new image filename
            cur.execute("UPDATE tbl_product SET image = %s WHERE id_product = %s", (new_filename, id_product))
            mysql.connection.commit()

        cur.close()
        flash("Data Successfully Updated", 'success')
        return redirect(url_for('product'))

    else:
        flash("You don't have permission to update this product.", 'danger')
        return redirect(url_for('product'))


# DELETE PRODUCT
def model_delete_product(id):
    if "loggedin" in session:
        id_user = session['id_user']
    else:
        flash("You must be logged in to delete a product.", "danger")
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_product WHERE id_product = %s AND id_user = %s", (id, id_user))
    data = cur.fetchone()

    if data:
        cur.execute("DELETE FROM tbl_product WHERE id_product = %s", (id,))
        mysql.connection.commit()
        cur.close()

        # Delete the product image if it exists
        if data[6]:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], data[6]))

        flash("Product Successfully Deleted", 'danger')
        return redirect(url_for('product'))
    else:
        flash("You don't have permission to delete this product.", 'danger')
        return redirect(url_for('product'))


# MOVE SENT PRODUCTS TO THE PRODUCTS PAGE AS UNLISTED
def move_sent_to_unlisted_product():
    if "loggedin" not in session:
        flash("You must be logged in to move products.", "danger")
        return redirect(url_for('login'))

    id_user = session['id_user']

    # Query to fetch 'Sent' products where the user is a seller
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT tbl_product.id_product, tbl_product.id_category, tbl_product.product_name,
        tbl_product.product_price, tbl_product.description,
        tbl_payment_transaction_detail.qty,
        tbl_product.image, tbl_product.id_user
        FROM tbl_payment_transaction
        JOIN tbl_payment_transaction_detail
            ON tbl_payment_transaction.id_transaction = tbl_payment_transaction_detail.id_transaction
        JOIN tbl_product ON tbl_payment_transaction_detail.id_product = tbl_product.id_product
        JOIN tbl_user ON tbl_product.id_user = tbl_user.id_user
        WHERE tbl_payment_transaction.order_status = 'sent'
        AND tbl_user.role = 'seller'
    """)
    sent_products = cur.fetchall()

    if sent_products:
        for product in sent_products:
            id_category = product[1]
            product_name = product[2]
            product_price = product[3]
            description = product[4] if product[4] else None
            product_stock = product[5]
            image = 'image.jpg'
            id_user = session['id_user']

            # Insert each 'Sent' product as 'Unlisted'
            cur.execute("""
                INSERT INTO tbl_product (id_category, product_name, product_price, description, product_stock, image, id_user, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'unlisted')
            """, (id_category, product_name, product_price, description, product_stock, image, id_user))

        # Commit the changes and close the cursor
        mysql.connection.commit()
        cur.close()

        flash("All 'Sent' products have been moved to 'Unlisted'.", "success")
    else:
        flash("No 'Sent' products found for the seller.", "danger")

    return redirect(url_for('product'))


# def move_sent_to_unlisted_product():
#     if "loggedin" not in session:
#         flash("You must be logged in to move products.", "danger")
#         return redirect(url_for('login'))

#     id_user = session['id_user']

#     # Query to fetch 'Sent' products for the logged-in seller only
#     cur = mysql.connection.cursor()
#     cur.execute("""
#         SELECT tbl_product.id_product, tbl_product.id_category, tbl_product.product_name,
#         tbl_product.product_price, tbl_product.description,
#         tbl_payment_transaction_detail.qty,
#         tbl_product.image, tbl_product.id_user
#         FROM tbl_payment_transaction
#         JOIN tbl_payment_transaction_detail
#             ON tbl_payment_transaction.id_transaction = tbl_payment_transaction_detail.id_transaction
#         JOIN tbl_product ON tbl_payment_transaction_detail.id_product = tbl_product.id_product
#         JOIN tbl_user ON tbl_product.id_user = tbl_user.id_user
#         WHERE tbl_payment_transaction.order_status = 'sent'
#         AND tbl_user.role = 'seller'
#         AND tbl_user.id_user = %s  -- Filter to only the logged-in seller
#     """, (id_user,))
#     sent_products = cur.fetchall()

#     if sent_products:
#         for product in sent_products:
#             id_category = product[1]
#             product_name = product[2]
#             product_price = product[3]
#             description = product[4] if product[4] else None
#             product_stock = product[5]
#             image = 'image.jpg'
#             id_user = session['id_user']

#             # Insert each 'Sent' product as 'Unlisted'
#             cur.execute("""
#                 INSERT INTO tbl_product (id_category, product_name, product_price, description, product_stock, image, id_user, status)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, 'unlisted')
#             """, (id_category, product_name, product_price, description, product_stock, image, id_user))

#         # Commit the changes and close the cursor
#         mysql.connection.commit()
#         cur.close()

#         flash("All your 'Sent' products have been moved to 'Unlisted'.", "success")
#     else:
#         flash("No 'Sent' products found for you.", "danger")

#     return redirect(url_for('product'))
