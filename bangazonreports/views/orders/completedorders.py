import sqlite3
from django.shortcuts import render
from bangazonapi.models import order, customer, orderproduct
from bangazonreports.views import Connection

def completedorder_list(request):
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

    db_cursor.execute("""
SELECT
    pt.merchant_name,
    SUM(p.price) total_price, 
    u.first_name || " " || u.last_name customer_name,
    o.id order_id
FROM bangazonapi_order o
    JOIN bangazonapi_customer c ON o.customer_id = c.id
    JOIN bangazonapi_orderproduct op ON o.id = op.order_id
    JOIN bangazonapi_product p ON p.id = op.product_id
    JOIN auth_user u ON u.id = c.user_id
    JOIN bangazonapi_payment pt ON pt.id = o.payment_type_id
    WHERE o.payment_type_id is not NULL
    GROUP BY order_id
    """)

    dataset = db_cursor.fetchall()
    completed_orders = {}

    for row in dataset:
        oid = row["order_id"]
        completed_orders[oid] = {}
        completed_orders[oid]["order_id"] = row["order_id"]
        completed_orders[oid]["customer_name"] = row["customer_name"]
        completed_orders[oid]["total_price"] = row["total_price"]
        completed_orders[oid]["merchant_name"] = row["merchant_name"]
        

    list_of_completed_orders = completed_orders.values()

    template = 'completed_orders_list.html'
    context = {

            'completedorder_list': list_of_completed_orders
    }

    return render(request, template, context)