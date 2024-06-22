import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect('shop.db')

def create_tables():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            address TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            description TEXT,
                            price REAL NOT NULL,
                            stock INTEGER NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            customer_id INTEGER,
                            order_date TEXT,
                            total REAL,
                            FOREIGN KEY (customer_id) REFERENCES customers(id))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS order_details (
                            order_id INTEGER,
                            product_id INTEGER,
                            quantity INTEGER,
                            price REAL,
                            FOREIGN KEY (order_id) REFERENCES orders(id),
                            FOREIGN KEY (product_id) REFERENCES products(id),
                            PRIMARY KEY (order_id, product_id))''')
        conn.commit()

def email_exists(email):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM customers WHERE email = ?', (email,))
        return cursor.fetchone() is not None

def add_customer(name, email, address):
    if email_exists(email):
        print(f"Customer with email {email} already exists.")
        return
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO customers (name, email, address) VALUES (?, ?, ?)', (name, email, address))
        conn.commit()

def update_customer(customer_id, name, email, address):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE customers 
                          SET name = ?, email = ?, address = ? 
                          WHERE id = ?''', (name, email, address, customer_id))
        conn.commit()

def delete_customer(customer_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        conn.commit()

def add_product(name, description, price, stock):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)', (name, description, price, stock))
        conn.commit()

def update_product(product_id, name, description, price, stock):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE products 
                          SET name = ?, description = ?, price = ?, stock = ? 
                          WHERE id = ?''', (name, description, price, stock, product_id))
        conn.commit()

def delete_product(product_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()

def create_order(customer_id, order_details):
    order_date = datetime.now().strftime('%Y-%m-%d')
    total = sum(item['quantity'] * item['price'] for item in order_details)
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO orders (customer_id, order_date, total) VALUES (?, ?, ?)', (customer_id, order_date, total))
        order_id = cursor.lastrowid
        for item in order_details:
            cursor.execute('INSERT INTO order_details (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)',
                           (order_id, item['product_id'], item['quantity'], item['price']))
            cursor.execute('UPDATE products SET stock = stock - ? WHERE id = ?', (item['quantity'], item['product_id']))
        conn.commit()

def get_orders():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT orders.id, customers.name AS customer, orders.order_date, orders.total
                          FROM orders
                          JOIN customers ON orders.customer_id = customers.id''')
        return cursor.fetchall()

def get_order_details(order_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT order_details.order_id, products.name AS product, order_details.quantity, order_details.price
                          FROM order_details
                          JOIN products ON order_details.product_id = products.id
                          WHERE order_details.order_id = ?''', (order_id,))
        return cursor.fetchall()

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

if __name__ == '__main__':
    create_tables()
    add_customer('John Doe', 'john@example.com', '123 Elm Street')
    add_customer('Jane Smith', 'jane@example.com', '456 Oak Avenue')
    add_product('Laptop', 'A high-end gaming laptop', 1500.00, 10)
    add_product('Smartphone', 'Latest model smartphone', 800.00, 20)
    add_product('Headphones', 'Noise-cancelling headphones', 200.00, 15)
    create_order(1, [{'product_id': 1, 'quantity': 1, 'price': 1500.00}, {'product_id': 3, 'quantity': 1, 'price': 200.00}])
    create_order(2, [{'product_id': 2, 'quantity': 1, 'price': 800.00}, {'product_id': 3, 'quantity': 1, 'price': 200.00}])

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
        details = get_order_details(order[0])
        for detail in details:
            print('  ', detail)

    print("\nUpdating Customer with ID 1...")
    update_customer(1, 'John Updated', 'john_updated@example.com', '789 New Street')
    print("All Customers After Update:")
    customers = get_customers()
    for customer in customers:
        print(customer)

    print("\nDeleting Customer with ID 2...")
    delete_customer(2)
    print("All Customers After Deletion:")
    customers = get_customers()
    for customer in customers:
        print(customer)

    print("\nUpdating Product with ID 1...")
    update_product(1, 'Laptop Updated', 'An updated high-end gaming laptop', 1600.00, 8)
    print("All Products After Update:")
    products = get_products()
    for product in products:
        print(product)

    print("\nDeleting Product with ID 3...")
    delete_product(3)
    print("All Products After Deletion:")
    products = get_products()
    for product in products:
        print(product)
