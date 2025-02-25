from flask import Flask, render_template, redirect, url_for, request, flash
import os
from db import mysql

# Routing to USER
def model_user():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM tbl_user")
  data = cur.fetchall()
  cur.close()
  return render_template('admin/user/user.html', data_user=data)

# ADD USER
def model_add_user():
  if request.method == "POST":
    user_name = request.form['form_user_name']
    user_age = request.form['form_user_age']
    user_telp = request.form['form_user_telp']
    user_address = request.form['form_user_address']
    user_email = request.form['form_user_email']
    user_role = request.form['form_user_role']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tbl_user VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                ('', '', '', user_name, user_age, user_telp, user_address, user_email, user_role))
    mysql.connection.commit()
    cur.close()

    flash("Data Successfully Added", "success")
    return redirect(url_for('user'))

  return render_template('admin/user/add_user.html')

# EDIT USER
def model_edit_user(id):
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM tbl_user WHERE id_user = %s", (id, ))
  data = cur.fetchone()
  return render_template('admin/user/edit_user.html', data_user=data)

# PROCESS EDIT USER
def model_process_edit_user():
  id_user = request.form['form_id_user']
  user_name = request.form['form_user_name']
  user_age = request.form['form_user_age']
  user_telp = request.form['form_user_telp']
  user_address = request.form['form_user_address']
  user_email = request.form['form_user_email']
  user_role = request.form['form_user_role']

  cur = mysql.connection.cursor()
  cur.execute("UPDATE tbl_user SET name = %s, age = %s, telp = %s, address = %s, email = %s, role = %s WHERE id_user = %s",
              (user_name, user_age, user_telp, user_address, user_email, user_role, id_user))
  mysql.connection.commit()
  cur.close()

  flash("Data Successfully Updated", "success")
  return redirect(url_for("user"))

# DELETE USER
def model_delete_user(id):
  cur = mysql.connection.cursor()
  cur.execute("DELETE FROM tbl_user WHERE id_user = %s", (id, ))
  mysql.connection.commit()
  cur.close()

  flash("Data Successfully Deleted", "danger")
  return redirect(url_for('user'))

