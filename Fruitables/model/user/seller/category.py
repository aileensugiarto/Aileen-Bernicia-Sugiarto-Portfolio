# from flask import Flask, render_template, redirect, url_for, request, flash
# import os
# from db import mysql


# # Routing to CATEGORY
# def model_category():
#   cur = mysql.connection.cursor()
#   cur.execute("SELECT * FROM tbl_category")
#   data = cur.fetchall()
#   cur.close()
#   return render_template('user/seller/category/category.html', data_category=data)

# # ADD CATEGORY
# def model_add_category():
#   if request.method == "POST":
#     category_name = request.form['form_name']
#     cur = mysql.connection.cursor()
#     cur.execute("INSERT INTO tbl_category VALUES (%s, %s)", ('', category_name))
#     mysql.connection.commit()
#     cur.close()

#     flash("Category Successfully Added", 'success')
#     return redirect(url_for('category'))

#   return render_template('user/seller/category/add_category.html')

# # EDIT CATEGORY
# def model_edit_category(id):
#   cur = mysql.connection.cursor()
#   cur.execute("SELECT * FROM tbl_category WHERE id_category = %s", (id, ))
#   data = cur.fetchone()
#   return render_template('user/seller/category/edit_category.html', data_category=data)

# # PROCESS EDIT CATEGORY
# def model_process_edit_category():
#   category_name = request.form['form_name']
#   id_category = request.form['form_id']
#   cur = mysql.connection.cursor()
#   cur.execute("UPDATE tbl_category SET category_name = %s WHERE id_category = %s", (category_name, id_category))
#   mysql.connection.commit()
#   cur.close()

#   flash("Data Successfully Updated", 'success')
#   return redirect(url_for('category'))

# # DELETE CATEGORY
# def model_delete_category(id):
#   cur = mysql.connection.cursor()
#   cur.execute("DELETE FROM tbl_category WHERE id_category = %s", (id, ))
#   mysql.connection.commit()
#   cur.close()

#   flash("Data Successfully Deleted", 'danger')
#   return redirect(url_for('category'))


from flask import Flask, render_template, redirect, url_for, request, flash
import os
from db import mysql
from flask import session

# Routing to CATEGORY
def model_category():
    if "loggedin" in session:
        id_user = session['id_user']  # Get the current logged-in user's ID
    else:
        flash("You must be logged in to view categories.", "danger")
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT *  FROM tbl_category c JOIN tbl_user u ON c.id_user = u.id_user WHERE u.id_user = %s", (id_user,))
    data = cur.fetchall()
    cur.close()
    return render_template('user/seller/category/category.html', data_category=data)

# ADD CATEGORY
def model_add_category():
    if request.method == "POST":
        category_name = request.form['form_name']

        if "loggedin" in session:
            id_user = session['id_user']  # Get the current logged-in user's ID
        else:
            flash("You must be logged in to add a category.", "danger")
            return redirect(url_for('login'))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbl_category (category_name, id_user) VALUES (%s, %s)", (category_name, id_user))
        mysql.connection.commit()
        cur.close()

        flash("Category Successfully Added", 'success')
        return redirect(url_for('category'))

    return render_template('user/seller/category/add_category.html')

# EDIT CATEGORY
def model_edit_category(id):
    if "loggedin" in session:
        id_user = session['id_user']  # Get the current logged-in user's ID
    else:
        flash("You must be logged in to edit a category.", "danger")
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_category WHERE id_category = %s AND id_user = %s", (id, id_user))
    data = cur.fetchone()

    if data:
        return render_template('user/seller/category/edit_category.html', data_category=data)
    else:
        flash("You don't have permission to edit this category.", "danger")
        return redirect(url_for('category'))

# PROCESS EDIT CATEGORY
def model_process_edit_category():
    if "loggedin" in session:
        id_user = session['id_user']  # Get the current logged-in user's ID
    else:
        flash("You must be logged in to update a category.", "danger")
        return redirect(url_for('login'))

    category_name = request.form['form_name']
    id_category = request.form['form_id']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_category WHERE id_category = %s AND id_user = %s", (id_category, id_user))
    data = cur.fetchone()

    if data:
        cur.execute("UPDATE tbl_category SET category_name = %s WHERE id_category = %s", (category_name, id_category))
        mysql.connection.commit()
        cur.close()

        flash("Category Successfully Updated", 'success')
        return redirect(url_for('category'))
    else:
        flash("You don't have permission to update this category.", "danger")
        return redirect(url_for('category'))

# DELETE CATEGORY
def model_delete_category(id):
    if "loggedin" in session:
        id_user = session['id_user']  # Get the current logged-in user's ID
    else:
        flash("You must be logged in to delete a category.", "danger")
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_category WHERE id_category = %s AND id_user = %s", (id, id_user))
    data = cur.fetchone()

    if data:
        cur.execute("DELETE FROM tbl_category WHERE id_category = %s", (id,))
        mysql.connection.commit()
        cur.close()

        flash("Category Successfully Deleted", 'danger')
        return redirect(url_for('category'))
    else:
        flash("You don't have permission to delete this category.", "danger")
        return redirect(url_for('category'))
