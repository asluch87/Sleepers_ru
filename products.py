# %s -Параметр передаваемый в запрос , чтобы чне лазить в гугл пишу тут.

from database import get_db_connection

def get_products(search='', min_price='', max_price=''):
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = "SELECT * FROM products WHERE 1=1"
    params = []
    
    if search:
        query += " AND (name ILIKE %s OR description ILIKE %s)"
        params.extend([f'%{search}%', f'%{search}%'])
    
    if min_price:
        query += " AND price >= %s"
        params.append(float(min_price))
    
    if max_price:
        query += " AND price <= %s" 
        params.append(float(max_price))
    
    query += " ORDER BY id DESC"
    cur.execute(query, params)
    products = cur.fetchall()
    
    cur.close()
    conn.close()
    return products

def get_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE id = %s', (product_id,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    return product

def get_basket_items(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT p.*, b.quantity FROM basket b 
        JOIN products p ON b.product_id = p.id 
        WHERE b.user_id = %s 
    ''', (user_id,))
    basket_items = cur.fetchall()
    total = sum(item[4] * item[5] for item in basket_items)
    cur.close()
    conn.close()
    return basket_items, total

def create_order_product(user_id, product_id, quantity):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Проверяем наличие
    cur.execute('SELECT stock_quantity FROM products WHERE id = %s', (product_id,))
    product = cur.fetchone()
    
    if not product or product[0] < quantity:
        return False
     
    # Добавляем в корзину
    cur.execute('''
            INSERT INTO basket (user_id, product_id, quantity) 
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, product_id) 
            DO UPDATE SET quantity = basket.quantity + EXCLUDED.quantity
        ''', (user_id, product_id, quantity))
    
    # Обновляем остатки
    cur.execute('UPDATE products SET stock_quantity = stock_quantity - %s WHERE id = %s',
               (quantity, product_id))
    
    conn.commit()
    cur.close()
    conn.close()
    return True


