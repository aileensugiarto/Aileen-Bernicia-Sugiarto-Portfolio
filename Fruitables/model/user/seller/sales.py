from flask import render_template, request, session
from db import mysql
from decimal import Decimal

def model_sales_report():
    id_user = session.get('id_user')

    if not id_user:
        return "User not logged in", 401

    # Get the category filter
    category_id = request.args.get('category')

    # Initialize query to get sales data
    query = """
        SELECT pt.transaction_date, p.product_name, ptd.qty, ptd.price,
        pt.total_price, p.id_category, p.id_product
        FROM tbl_payment_transaction pt
        JOIN tbl_payment_transaction_detail ptd ON pt.id_transaction = ptd.id_transaction
        JOIN tbl_product p ON p.id_product = ptd.id_product
        WHERE pt.order_status IN ('packaging', 'delivery', 'sent')
        AND p.id_user = %s
    """
    filters = [id_user]

    # Add filter for category
    if category_id:
        query += " AND p.id_category = %s"
        filters.append(category_id)

    query += " GROUP BY pt.id_transaction, p.product_name, ptd.qty, ptd.price, p.id_category, p.id_product"

    cur = mysql.connection.cursor()
    cur.execute(query, tuple(filters))
    sales_data = cur.fetchall()

    # Calculate total sales (using total_price column)
    total_sales = sum(Decimal(sale[4]) for sale in sales_data) if sales_data else Decimal('0')  # Convert to Decimal
    items_sold = sum(sale[2] for sale in sales_data) if sales_data else 0  # Total quantity sold

    # Calculate total sales after 10% admin commission
    new_total_sales = total_sales * Decimal('0.90')  # Ensuring precision with Decimal

    # For best-selling product, check if sales_data is not empty
    if sales_data:
        best_selling_product = max(sales_data, key=lambda x: x[2])[1]  # Product name with highest quantity sold
    else:
        best_selling_product = "No sales"

    # Fetch product categories for filter dropdown
    cur.execute("SELECT id_category, category_name FROM tbl_category")
    categories = cur.fetchall()

    return render_template(
        'user/seller/sales/sales.html',
        sales_data=sales_data,
        total_sales=total_sales,
        new_total_sales=new_total_sales,
        items_sold=items_sold,
        best_selling_product=best_selling_product,
        categories=categories
    )
