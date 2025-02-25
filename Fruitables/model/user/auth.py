from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
import os, requests, midtransclient, uuid
from db import mysql
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'aileen'
app.config['UPLOAD_FOLDER'] = 'static/uploads/proof'

# Rajaongkir
RAJAONGKIR_API_KEY = '71bd102318358b6da806fe670361d8e3'
RAJAONGKIR_BASE_URL = 'https://api.rajaongkir.com/starter/'

# Midtrans
MIDTRANS_SERVER_KEY = 'SB-Mid-server-yjvhbAPLBG-ruQXs6tsbrTxW'
MIDTRANS_CLIENT_KEY = 'SB-Mid-client-LL2rEblyeJMYdTz4'

# REGISTER USER
def model_register_user():
  if request.method == 'POST':
    username = request.form['form_username']
    password = request.form['form_password']
    name = request.form['form_name']
    age = request.form['form_age']
    telp = request.form['form_telp']
    address = request.form['form_address']
    email = request.form['form_email']
    role = request.form['form_role']
    cur = mysql.connection.cursor()

    # Check Username
    cur.execute("SELECT * FROM tbl_user WHERE username = %s", (username, ))
    account = cur.fetchone()

    if account is None:
      cur.execute("INSERT INTO tbl_user VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", ('', username, password, name, age, telp, address, email, role))
      mysql.connection.commit()
      flash("Register Successful", 'success')
      return redirect(url_for('login'))

    else:
      flash("Username Already Exists", 'danger')
      return redirect(url_for('register'))

  return render_template('user/register.html')

def model_login_user():
  if request.method == 'POST':
    username = request.form['form_username']
    password = request.form['form_password']
    cur = mysql.connection.cursor()
    # Retrieve the user by username
    cur.execute("SELECT * FROM tbl_user WHERE username = %s", (username,))
    account = cur.fetchone()
    if account is None:
      flash("Login Failed. Check Your Username", 'danger')
    elif password != account[2]:  # Assuming password is at index 2
      flash("Login Failed. Check Your Password", 'danger')
    else:
      # If login is successful, store user data in the session
      session['loggedin'] = True
      session['name'] = account[3]  # Assuming name is at index 3
      session['id_user'] = account[0]  # Assuming id_user is at index 0
      user_role = account[8]  # Assuming role is at index 8
      # Redirect based on user role
      if user_role == 'seller':
          return redirect(url_for('seller_home'))  # Redirect to seller dashboard
      else:
          return redirect(url_for('buyer_home'))  # Redirect to buyer home
  return render_template('user/login.html')

# LOGOUT USER
def model_logout_user():
  session.pop('loggedin', None)
  session.pop('name', None)
  return redirect(url_for('login'))