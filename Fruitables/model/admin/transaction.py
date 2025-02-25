from flask import Flask, render_template, redirect, url_for, request, flash
import os
from db import mysql

# Routing to TRANSACTION
def model_transaction():
  cur = mysql.connection.cursor()
  cur.execute("SELECT a.*, b.name FROM tbl_payment_transaction a JOIN tbl_user b ON a.id_user = b.id_user WHERE a.order_status = 'billing'")
  data_billing = cur.fetchall()

  cur.execute("SELECT a.*, b.name FROM tbl_payment_transaction a JOIN tbl_user b ON a.id_user = b.id_user WHERE a.order_status = 'packaging'")
  data_packaging = cur.fetchall()

  cur.execute("SELECT a.*, b.name FROM tbl_payment_transaction a JOIN tbl_user b ON a.id_user = b.id_user WHERE a.order_status = 'delivery'")
  data_delivery = cur.fetchall()

  cur.execute("SELECT a.*, b.name FROM tbl_payment_transaction a JOIN tbl_user b ON a.id_user = b.id_user WHERE a.order_status = 'sent'")
  data_sent = cur.fetchall()

  return render_template('admin/transaction/transaction.html',
                        data_transaction_billing=data_billing, data_transaction_packaging=data_packaging, data_transaction_delivery=data_delivery, data_transaction_sent=data_sent)


# PROCESS DELIVERY
def model_process_delivery():
  id_transaction = request.form['form_id_transaction']
  cur = mysql.connection.cursor()
  cur.execute("UPDATE tbl_payment_transaction SET order_status = %s WHERE id_transaction = %s", ('delivery', id_transaction))
  mysql.connection.commit()

  cur.close()
  return redirect(url_for('transaction'))


# PROCESS SENT
def model_process_sent():
  id_transaction = request.form['form_id_transaction']
  cur = mysql.connection.cursor()
  cur.execute("UPDATE tbl_payment_transaction SET order_status = %s WHERE id_transaction = %s", ('sent', id_transaction))
  mysql.connection.commit()

  cur.close()
  return redirect(url_for('transaction'))


# DETAIL TRANSACTION
def model_detail_transaction(id_transaction):
  cur = mysql.connection.cursor()
  cur.execute("""SELECT a.*, b.province_name, c.city_name FROM tbl_payment_transaction a
              JOIN tbl_provinces b ON a.province = b.id_province JOIN tbl_cities c ON a.city
              WHERE id_transaction = %s""",[id_transaction])
  data_transaction = cur.fetchone()
  mysql.connection.commit()

  cur.execute("SELECT b.* FROM tbl_payment_transaction a JOIN tbl_user b ON a.id_user = b.id_user WHERE id_transaction = %s", [id_transaction])
  data_user = cur.fetchone()
  mysql.connection.commit()

  cur.execute("""SELECT a.id_product, a.qty, a.price, tbl_product.product_name from tbl_payment_transaction_detail a
              JOIN tbl_product on a.id_product = tbl_product.id_product WHERE a.id_transaction = %s""", [id_transaction])
  data_product = cur.fetchall()
  mysql.connection.commit()

  cur.execute("SELECT total_price FROM tbl_payment_transaction WHERE id_transaction = %s", [id_transaction])
  total = cur.fetchone()
  mysql.connection.commit()

  cur.close()
  return render_template('admin/transaction/detail_transaction.html',
                        data_product=data_product, data_transaction=data_transaction, total_price=total, data_user=data_user)

