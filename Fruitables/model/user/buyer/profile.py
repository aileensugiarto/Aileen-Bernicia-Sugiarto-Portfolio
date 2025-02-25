from flask import Flask, render_template, redirect, url_for, request, flash, session
import os
from db import mysql

app = Flask(__name__)
app.secret_key = 'aileen'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Get USER
def get_user():
  cur = mysql.connection.cursor()
  cur.execute("SELECT * FROM tbl_user")
  users = cur.fetchall()
  cur.close()
  return users

# PROFILE
def model_profile():
  id_user = session.get('id_user')
  if not id_user:
    flash('Please Login', 'danger')
    return redirect(url_for('login'))

  cur = mysql.connection.cursor()
  cur.execute("""
    SELECT u.id_user, u.name, u.username, u.telp, u.address, u.email, u.role,
    p.bio, p.profile_picture
    FROM tbl_user u
    LEFT JOIN tbl_profile p ON u.id_user = p.id_user
    WHERE u.id_user = %s
  """, (id_user,))
  data = cur.fetchone()
  cur.close()

  return render_template('user/buyer/profile.html', data_profile=data)

# EDIT PROFILE
def model_edit_profile(id_user):
  cur = mysql.connection.cursor()
  cur.execute("""
    SELECT u.id_user, u.name, u.username, u.telp, u.address, u.email, u.role,
    p.id_profile, p.bio, p.profile_picture
    FROM tbl_user u
    LEFT JOIN tbl_profile p ON u.id_user = p.id_user
    WHERE u.id_user = %s
  """, (id_user,))
  data = cur.fetchone()
  cur.close()

  return render_template('user/buyer/edit_profile.html', data_profile=data)

# PROCESS EDIT PROFILE
def model_process_edit_profile():
  id_user = request.form['form_id_user']
  name = request.form['form_name']
  username = request.form['form_username']
  telp = request.form['form_telp']
  address = request.form['form_address']
  email = request.form['form_email']
  bio = request.form['form_bio']

  cur = mysql.connection.cursor()
  cur.execute("""
    UPDATE tbl_user
    SET name = %s, username = %s, telp = %s, address = %s, email = %s
    WHERE id_user = %s
  """, (name, username, telp, address, email, id_user))

  mysql.connection.commit()

  # Update or insert profile details in tbl_profile
  cur.execute("SELECT id_profile FROM tbl_profile WHERE id_user = %s", (id_user,))

  profile_exists = cur.fetchone()

  if profile_exists:
    cur.execute("UPDATE tbl_profile SET bio = %s WHERE id_user = %s", (bio, id_user))
  else:
    cur.execute("INSERT INTO tbl_profile (id_user, bio) VALUES (%s, %s)", (id_user, bio))

  mysql.connection.commit()

  # Handle profile picture upload
  file = request.files['form_profile_picture']
  filename = file.filename

  if file and filename:
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    cur.execute("""
        UPDATE tbl_profile
        SET profile_picture = %s
        WHERE id_user = %s
    """, (filename, id_user))

    mysql.connection.commit()

  cur.close()

  flash("Profile Successfully Updated", 'success')
  return redirect(url_for('profile'))
