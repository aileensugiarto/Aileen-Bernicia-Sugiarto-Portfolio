from flask import Flask, render_template, redirect, url_for, request, flash, session
from db import mysql

def model_login():
  if request.method == 'POST':
    username = request.form['form_username']
    password = request.form['form_password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tbl_admin WHERE username = %s", (username,))

    account = cur.fetchone()
    if account is None:
      flash("Login Failed. Please check your username.", "danger")
    elif password != account[2]:
      flash("Login Failed. Please check your password.", "danger")
    else:
      session["loggedin"] = True
      session["name"] = account[3]
      return redirect(url_for("dashboard"))

  return render_template('admin/login_admin.html')

def model_logout():
  session.pop('loggedin', None)
  session.pop('name', None)
  return redirect(url_for('login_admin'))