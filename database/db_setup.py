import os
import sqlite3

def setup_database():
    # Create database directory if it doesn't exist
    os.makedirs('database', exist_ok=True)
    
    # Connect to database
    db_path = os.path.join('database', 'inventory.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku_id TEXT NOT NULL,
            barcode TEXT,
            category TEXT NOT NULL,
            subcategory TEXT,
            product_name TEXT NOT NULL,
            description TEXT,
            tax_rate REAL NOT NULL,
            price REAL NOT NULL,
            default_unit TEXT NOT NULL,
            image_path TEXT,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(sku_id, user_id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create suppliers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, user_id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(name, user_id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create goods_receiving table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goods_receiving (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier TEXT NOT NULL,
            product_sku TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            rate REAL NOT NULL,
            tax_rate REAL NOT NULL,
            total_rate REAL NOT NULL,
            tax_amount REAL NOT NULL,
            total_amount REAL NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL,
            product_sku TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            rate REAL NOT NULL,
            tax_rate REAL NOT NULL,
            total_rate REAL NOT NULL,
            tax_amount REAL NOT NULL,
            total_amount REAL NOT NULL,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Create default admin user if it doesn't exist
    cursor.execute("SELECT id FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (username, password, email, name)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin123', 'admin@example.com', 'Administrator'))
    
    conn.commit()
    conn.close() 