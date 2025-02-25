import decimal
from flask import render_template
from db import mysql

def admin_earnings():
    # Query to get total sales for each seller along with their names
    query = """
        SELECT u.username, SUM(pt.total_price) as total_sales
        FROM tbl_payment_transaction pt
        JOIN tbl_payment_transaction_detail ptd ON pt.id_transaction = ptd.id_transaction
        JOIN tbl_product p ON p.id_product = ptd.id_product
        JOIN tbl_user u ON p.id_user = u.id_user
        WHERE pt.order_status IN ('sent', 'delivery', 'packaging')
        GROUP BY u.id_user, u.username
    """

    # Execute query to get sellers' total sales
    cur = mysql.connection.cursor()
    cur.execute(query)
    sales_data = cur.fetchall()

    # Initialize admin's total earnings
    admin_earnings = decimal.Decimal('0.00')

    # Process seller earnings and admin commission breakdown
    earnings_breakdown = []
    for index, sale in enumerate(sales_data, start=1):
        seller_name = sale[0]
        seller_sales = sale[1]  # Total sales for the seller
        admin_commission = seller_sales * decimal.Decimal('0.10')  # Admin takes 10%
        seller_earnings_after_commission = seller_sales - admin_commission  # Seller earnings after 10%

        # Append to breakdown list
        earnings_breakdown.append({
            "no": index,
            "seller_name": seller_name,
            "total_sales": seller_sales,
            "seller_earnings_after_commission": seller_earnings_after_commission,
            "admin_commission": admin_commission
        })

        # Add to admin total earnings
        admin_earnings += admin_commission

    # Return the rendered earnings page
    return render_template(
        'admin/earnings/earnings.html',
        admin_earnings=admin_earnings,
        earnings_breakdown=earnings_breakdown
    )

