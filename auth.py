from flask import request, session, flash, redirect, url_for, render_template
from database import get_db_connection
import hashlib
from models import User
from sqlalchemy.exc import SQLAlchemyError

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user():
    first_name_form = request.form['first_name']
    password_form = request.form['password']
    hash_password_form = hash_password(password_form)
    session_WEB = get_db_connection() 
    
    try:
        userrs_obj = session_WEB.query(User).filter(
            User.password_hash == hash_password_form, 
            User.first_name == first_name_form  
        ).first()

        if userrs_obj:
            session['id'] = userrs_obj.id
            session['first_name'] = userrs_obj.first_name
            session['role_id'] = userrs_obj.role_id
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неверный логин или пароль', 'error')
            return render_template('login.html')
    
    finally:
        session_WEB.close()

def register_user():
    first_name_form = request.form['first_name']
    last_name_form = request.form['last_name']
    password_form = hash_password(request.form['password'])
    email_form = request.form['email']
    Session_DB = get_db_connection()
    
    try:
        find_user = Session_DB.query(User).filter(User.email == email_form).first()

        if find_user:
            flash('Пользователь с таким email уже зарегистрирован', 'error')
            return render_template('register.html')
        
        userrs_obj = User(
            first_name=first_name_form, 
            last_name=last_name_form,
            password_hash=password_form, 
            email=email_form,
            role_id=1
        )
         
        Session_DB.add(userrs_obj)
        Session_DB.commit()
        flash(f'Пользователь {userrs_obj.first_name} зарегистрирован', 'success')
        return redirect(url_for('login'))
        
    except Exception as e:
        Session_DB.rollback()
        flash(f'Ошибка при регистрации: {str(e)}', 'error')
        return render_template('register.html')
    finally:
        Session_DB.close()

def logout_user():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

def edit_profil_users():
    if request.method != 'POST':
        return False
    if 'id' not in session:
        flash('Требуется авторизация', 'error')
        return False
    
    first_name_form = request.form.get('first_name')
    last_name_form = request.form.get('last_name')
    email_form = request.form.get('email')
    phone_number_form = request.form.get('phone_number')
    current_user_id = session['id']
    
    session_BD = get_db_connection()
    
    try:
        current_user = session_BD.query(User).filter(User.id == current_user_id).first()
        if not current_user:
            flash('Пользователь не найден', 'error')
            return False
        
        if email_form != current_user.email:
            existing_user = session_BD.query(User)\
                .filter(
                    User.email == email_form,
                    User.id != current_user_id  
                )\
                .first()
            if existing_user:
                flash('Этот email уже используется другим пользователем', 'error')
                return False
        
        current_user.first_name = first_name_form
        current_user.last_name = last_name_form
        current_user.email = email_form
        if phone_number_form is not None:
            current_user.phone_number = phone_number_form
        
        session_BD.commit()
        
        session['first_name'] = first_name_form
        session['email'] = email_form
        
        flash('Профиль успешно обновлен', 'success')
        return True  
        
    except SQLAlchemyError as e:
        session_BD.rollback()
        flash(f'Ошибка базы данных: {str(e)}', 'error')
        return False
    finally:
        session_BD.close()

def get_user_by_id(user_id):
    session_DB = None
    try:
        session_DB = get_db_connection()
        user = session_DB.query(User).filter(User.id == user_id).first()
        return user
    except Exception as e:
        print(f"Ошибка при получении пользователя: {e}")
        return None
    finally:
        if session_DB:
            session_DB.close()

def delete_user_profile(user_id):
    if 'id' not in session:
        flash('Требуется авторизация', 'error')
        return False
    
    if session['id'] != user_id:
        flash('Можно удалить только свой профиль', 'error')
        return False
    
    session_DB = None
    try:
        session_DB = get_db_connection()
        user = session_DB.query(User).filter(User.id == user_id).first()
        
        if not user:
            flash('Пользователь не найден', 'error')
            return False
        
        session_DB.delete(user)
        session_DB.commit()
        
        session.clear()
        flash('Профиль успешно удален', 'success')
        return True
        
    except SQLAlchemyError as e:
        if session_DB:
            session_DB.rollback()
        flash(f'Ошибка базы данных при удалении: {str(e)}', 'error')
        return False
    except Exception as e:
        if session_DB:
            session_DB.rollback()
        flash(f'Неожиданная ошибка: {str(e)}', 'error')
        return False
    finally:
        if session_DB:
            session_DB.close()