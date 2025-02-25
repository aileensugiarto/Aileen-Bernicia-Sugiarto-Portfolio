from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
import os, requests, midtransclient, uuid
from db import mysql
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'aileen'
app.config['UPLOAD_FOLDER'] = 'static/uploads/bukti'

# Rajaongkir untuk pengiriman
RAJAONGKIR_API_KEY = '71bd102318358b6da806fe670361d8e3'
RAJAONGKIR_BASE_URL = 'https://api.rajaongkir.com/starter/'

MIDTRANS_SERVER_KEY = 'SB-Mid-server-yjvhbAPLBG-ruQXs6tsbrTxW'
MIDTRANS_CLIENT_KEY = 'SB-Mid-client-LL2rEblyeJMYdTz4'

# ORDER
def model_order(id_user):
    cur = mysql.connection.cursor()

    # Billing not the problem
    cur.execute("""
        SELECT pt.information, pt.transaction_date, pt.total_price, pt.order_status,
        pt.id_transaction, p.image, p.product_name, ptd.qty
        FROM tbl_payment_transaction pt
        JOIN tbl_payment_transaction_detail ptd ON pt.id_transaction = ptd.id_transaction
        JOIN tbl_product p ON ptd.id_product = p.id_product
        WHERE pt.order_status = 'billing' AND pt.id_user = %s
    """, (id_user, ))
    data_billing = cur.fetchall()

    # Packaging
    cur.execute("""
        SELECT pt.information, pt.transaction_date, pt.total_price, pt.order_status,
        pt.id_transaction, p.image, p.product_name, ptd.qty
        FROM tbl_payment_transaction pt
        JOIN tbl_payment_transaction_detail ptd ON pt.id_transaction = ptd.id_transaction
        JOIN tbl_product p ON ptd.id_product = p.id_product
        WHERE pt.order_status = 'packaging' AND pt.id_user = %s
    """, (id_user, ))
    data_packaging = cur.fetchall()

    # Delivery
    cur.execute("""
        SELECT pt.information, pt.transaction_date, pt.total_price, pt.order_status,
        pt.id_transaction, p.image, p.product_name, ptd.qty
        FROM tbl_payment_transaction pt
        JOIN tbl_payment_transaction_detail ptd ON pt.id_transaction = ptd.id_transaction
        JOIN tbl_product p ON ptd.id_product = p.id_product
        WHERE pt.order_status = 'delivery' AND pt.id_user = %s
    """, (id_user, ))
    data_delivery = cur.fetchall()

    # Sent
    cur.execute("""
        SELECT pt.information, pt.transaction_date, pt.total_price, pt.order_status,
        pt.id_transaction, p.image, p.product_name, ptd.qty
        FROM tbl_payment_transaction pt
        JOIN tbl_payment_transaction_detail ptd ON pt.id_transaction = ptd.id_transaction
        JOIN tbl_product p ON ptd.id_product = p.id_product
        WHERE pt.order_status = 'sent' AND pt.id_user = %s
    """, (id_user, ))
    data_sent = cur.fetchall()

    cur.close()

    return render_template('user/buyer/order.html',
                            data_transaction_billing=data_billing, data_transaction_packaging=data_packaging,
                            data_transaction_delivery=data_delivery, data_transaction_sent=data_sent)


# MODEL BILLING
def model_billing():
    transaction_id = request.form['form_id_transaction']

    snap = midtransclient.Snap(
        is_production=False,
        server_key=MIDTRANS_SERVER_KEY,
        client_key=MIDTRANS_CLIENT_KEY
    )

    # Fetching the items in the transaction
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT a.id_product, a.qty, tbl_payment_transaction.total_price, tbl_product.product_name
        FROM tbl_payment_transaction_detail a
        JOIN tbl_product ON a.id_product = tbl_product.id_product
        JOIN tbl_payment_transaction ON a.id_transaction = tbl_payment_transaction.id_transaction
        WHERE a.id_transaction = %s
    """, [transaction_id])
    items = cur.fetchall()

    # Ensure total_price is correctly retrieved from tbl_payment_transaction
    total_price = sum(item[2] for item in items)  # Use the total price from the transaction table

    item_details = []
    for item in items:
        unit_price = int(item[2]) // int(item[1])  # Calculate the unit price correctly
        item_details.append({
            "id": item[0],
            "price": unit_price,
            "quantity": int(item[1]),
            "name": item[3]
        })

    unique_order_id = f"{transaction_id}_{uuid.uuid4()}"

    # Prepare the parameters for Midtrans transaction
    param = {
        "transaction_details": {
            "order_id": unique_order_id,
            "gross_amount": total_price
        },
        "item_details": item_details,
        "credit_card": {
            "secure": True
        },
        "customer_details": {
            "first_name": 'Anonymous',
            "last_name": '',
            "email": 'customer@gmail.com',
            "phone": '0912309834'
        }
    }

    # Create the transaction on Midtrans
    transaction = snap.create_transaction(param)
    transaction_token = transaction['token']

    # Return the transaction token and other details
    return jsonify({'token': transaction_token, 'transaction_id': transaction_id, 'total_price': total_price})


# SAVE PAYMENT INFO
def model_save_payment_info():
  try:
    # Get the data from the request (the total price and transaction ID from the Midtrans popup)
    data = request.get_json()
    transaction_id = data['transaction_id']
    total_price = data['total_price']

    # Ensure total_price is correct and greater than zero
    if total_price <= 0:
        raise ValueError("Invalid total price")

    # Insert payment information into tbl_payment
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO tbl_payment (id_transaction, total_payment, payment_status, payment_method) "
        "VALUES (%s, %s, %s, %s)",
        (transaction_id, total_price, 'paid', 'transfer')
    )
    mysql.connection.commit()

    # Update the payment status in tbl_payment_transaction
    cur.execute(
        "UPDATE tbl_payment_transaction SET order_status = %s WHERE id_transaction = %s",
        ('packaging', transaction_id)
    )
    mysql.connection.commit()

    # Close the cursor and return a success response
    cur.close()
    return jsonify({'status': 'success'})

  except Exception as e:
    print('Error occurred: ', e)
    return jsonify({'error': str(e)}), 500