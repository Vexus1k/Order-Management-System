import sqlite3

def connect():
    return sqlite3.connect('shop.db')

def reset_database():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS order_details')
        cursor.execute('DROP TABLE IF EXISTS orders')
        cursor.execute('DROP TABLE IF EXISTS products')
        cursor.execute('DROP TABLE IF EXISTS customers')
        cursor.execute('''CREATE TABLE customers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            address TEXT)''')
        cursor.execute('''CREATE TABLE products (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            description TEXT,
                            price REAL NOT NULL,
                            stock INTEGER NOT NULL)''')
        cursor.execute('''CREATE TABLE orders (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            customer_id INTEGER,
                            order_date TEXT,
                            total REAL,
                            FOREIGN KEY (customer_id) REFERENCES customers(id))''')
        cursor.execute('''CREATE TABLE order_details (
                            order_id INTEGER,
                            product_id INTEGER,
                            quantity INTEGER,
                            price REAL,
                            FOREIGN KEY (order_id) REFERENCES orders(id),
                            FOREIGN KEY (product_id) REFERENCES products(id),
                            PRIMARY KEY (order_id, product_id))''')
        conn.commit()

if __name__ == '__main__':
    reset_database()
    print("Database has been reset.")
