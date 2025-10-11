from flask import request, session, flash, redirect, url_for, render_template
from database import get_db_connection
import hashlib
from models import User

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user():
    first_name_form = request.form['first_name'] #Получаем имя пользователя с формы
    password_form = request.form['password']#Получаем пароль с формы
    hash_password_form = hash_password(password_form) #хешируем пароль для сравнения в сессиях


    session_WEB = get_db_connection() 
    userrs_obj = session_WEB.query(User).filter(User.password_hash == hash_password_form,first_name_form == User.first_name).first()

#Проверяем а тот ли пользователь логиниться и запоминаем его в сессию.
    if userrs_obj:
        session['id'] = userrs_obj.id
        session['first_name'] = userrs_obj.first_name
        session['role_id'] = userrs_obj.role_id
        flash('Вы успешно вошли!', 'success')
        return redirect(url_for('index'))
    else:
            flash('Неверный логин или пароль', 'error')
            return render_template('login.html')
    session_WEB.close()


def register_user():
    first_name_form = request.form['first_name']
    last_name_form = request.form['last_name']
    password_form = hash_password(request.form['password'])
    email_form = request.form['email']
    Session_DB = get_db_connection()
    try:
       find_user = Session_DB.query(User).filter(User.email == email_form).first() # находим пользаказ с ткаим email если есть

       if find_user: # Проверяем если с таким email есть то выводим ошибку считаем что email повторятся не может
            flash('Пользователь с таким email уже зарегестрирован', 'error')
            Session_DB.close()
            return render_template('register.html')
        #Если не нашли то пишем в базу
       userrs_obj = User(first_name = first_name_form, last_name = last_name_form,password_hash = password_form, email = email_form,role_id = 1 )
         
       Session_DB.add(userrs_obj)
       Session_DB.commit()
       flash(f'Пользователь {userrs_obj.first_name} зарегестрирован')
       Session_DB.close()
       return redirect(url_for('login'))
    except Exception as e: # Если к примеру что то пошло не так то показываем exception
        Session_DB.rollback()
        flash(f'Ошибка при регистрации: {str(e)}', 'error')
        Session_DB.close()
        return render_template('register.html')
    
 

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
        
        # Проверяем email только если он изменился
        if email_form != current_user.email:
            existing_user = session_BD.query(User)\
                .filter(
                    User.email == email_form,
                    User.id != current_user_id  
                )\
                .first()
            if existing_user:
                flash('Этот email уже используется другим пользователем', 'error')
                return False  # ← Только здесь возвращаем False
        
        # Обновляем данные (достигается только если email проверка пройдена)
        current_user.first_name = first_name_form
        current_user.last_name = last_name_form
        current_user.email = email_form
        if phone_number_form is not None:  # Добавляем phone_number
            current_user.phone_number = phone_number_form
        
        session_BD.commit()
        
        # Обновляем сессию
        session['first_name'] = first_name_form
        session['email'] = email_form
        
        flash('Профиль успешно обновлен', 'success')
        return True  
        
    except Exception as e:
        session_BD.rollback()
        flash(f'Ошибка обновления: {str(e)}', 'error')
        return False
    finally:
        session_BD.close()    

def get_user_by_id(user_id):  #Находим пользователя
    try:
        session_DB = get_db_connection()
        user = session_DB.query(User).filter(User.id == user_id).first()
        return user
    except Exception as e:
        print(f"Ошибка при получении пользователя: {e}")
        return None
    finally:
        session_DB.close()        


def delete_user_profile(user_id):
    if 'id' not in session:
        flash('Требуется авторизация', 'error')
        return False
    
    # Проверяем права: можно удалить только свой профиль
    if session['id'] != user_id:
        flash('Можно удалить только свой профиль', 'error')
        return False
    
    session_DB = get_db_connection()
    
    try:
        user = session_DB.query(User).filter(User.id == user_id).first()
        
        if not user:
            flash('Пользователь не найден', 'error')
            return False
        
        session_DB.delete(user)
        session_DB.commit()
        
        # Очищаем сессию после удаления профиля
        session.clear()
        
        flash('Профиль успешно удален', 'success')
        return True
        
    except Exception as e:
        session_DB.rollback()
        flash(f'Ошибка удаления: {str(e)}', 'error')
        return False
    finally:
        session_DB.close()        
        
        

      





    