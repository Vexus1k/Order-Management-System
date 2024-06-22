import sqlite3

def connect():
    return sqlite3.connect('shop.db')

def get_customers():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers')
        return cursor.fetchall()

def get_products():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        return cursor.fetchall()

def get_orders():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT orders.id, customers.name AS customer, orders.order_date, orders.total
                          FROM orders
                          JOIN customers ON orders.customer_id = customers.id''')
        return cursor.fetchall()

def get_order_details():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT order_details.order_id, products.name AS product, order_details.quantity, order_details.price
                          FROM order_details
                          JOIN products ON order_details.product_id = products.id''')
        return cursor.fetchall()

if __name__ == '__main__':
    print("All Customers:")
    customers = get_customers()
    for customer in customers:
        print(customer)

    print("\nAll Products:")
    products = get_products()
    for product in products:
        print(product)

    print("\nAll Orders:")
    orders = get_orders()
    for order in orders:
        print(order)

    print("\nAll Order Details:")
    order_details = get_order_details()
    for detail in order_details:
        print(detail)
