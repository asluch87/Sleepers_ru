from flask import request, session
from database import get_db_connection

def admin_panel():
    conn = get_db_connection()
    cur = conn.cursor()
         
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    
    cur.close()
    conn.close()
    return users

def add_product():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    supplier = request.form['supplier']
     
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO products (name, description, price, stock, supplier) VALUES (%s, %s, %s, %s, %s)',
               (name, description, price, stock, supplier))
    conn.commit()
    cur.close()
    conn.close()
    return True

def delete_product(product_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM products WHERE id = %s', (product_id,))
    conn.commit()
    cur.close()
    conn.close()
    return True