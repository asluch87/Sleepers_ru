from flask import request, session, flash, redirect, url_for, render_template
from database import get_db_connection
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user():
    first_name = request.form['first_name']
    password = request.form['password']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE first_name = %s AND password_hash  = %s', 
               (first_name, hash_password(password)))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user:
        session['id'] = user[0]
        session['first_name'] = user[1]
        session['role_id'] = user[6]
        flash('Вы успешно вошли!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Неверный логин или пароль', 'error')
        return render_template('login.html')

def register_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']
    email = request.form['email']
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(''' 
            INSERT INTO users (first_name, last_name, email, password_hash, role_id) 
            VALUES (%s, %s, %s, %s, %s)
             ''', (first_name, last_name, email, hash_password(password), 1))
        conn.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('login'))
    except:
        flash('Имя пользователя занято', 'error')
        return render_template('register.html') 
    finally:
        cur.close()
        conn.close()

def logout_user():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))