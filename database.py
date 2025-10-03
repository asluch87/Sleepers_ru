import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host='192.168.1.132',
        database='PROD_Suppliers', 
        user='postgres',
        password='admin'
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()


     # Таблица для анонимных корзин (сессионные корзины)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS anonymous_basket (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(255) NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
            )
            ''')
    
   

    
    # Тестовые данные
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        cur.execute('''
            INSERT INTO products (name, slug, description, price, stock_quantity, sku)
            VALUES 
            ('Тапочки белые', 'white-slippers', 'Мягкие белые тапочки', 15.50, 100, 'SLIP-WHITE-001'),
           ('Тапочки синие', 'blue-slippers', 'Плотные синие тапочки', 18.00, 50, 'SLIP-BLUE-001')
             ''')
    

    conn.commit()
    cur.close()
    conn.close()