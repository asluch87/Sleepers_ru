from flask import request, session
from database import get_db_connection
from models import User,Product
from sqlalchemy import Time

def admin_panel():
    try:
        Session_DB = get_db_connection()
        admins = Session_DB.query(User).filter(User.role_id == 2 ).all()
        return admins
    finally:
        Session_DB.close() 

    
        
# Добавление товара в Админке
def add_products():
    try:
        
        # Получаем данные с формы
        name_form = request.form['name']
        description_form = request.form['description']
        price_form = float(request.form['price'])
        stock_form = int(request.form['stock'])
        supplier_form = request.form['supplier']
        
       
        
        # Создаем slug из названия
        slug = name_form.lower().replace(' ', '-')
        
        # Генерируем SKU
        sku = f"SLIP-{name_form.upper().replace(' ', '-')}-001"

        # Открываем сессию с БД для работы с БД
        Session_DB = get_db_connection()
             # Готовим объект экземпляра класса
        new_product = Product(
            name=name_form,
            slug=slug,
            description=description_form,
            price=price_form,
            stock_quantity=stock_form,
            stock=stock_form,
            sku=sku,
            is_active=True,
            supplier=supplier_form,
            image_url='https://via.placeholder.com/300x200?text=No+Image'
        )
                # Добавляем в БД
        Session_DB.add(new_product)
        Session_DB.commit() # коммитим
        
        return True
        
    except Exception as e:
        if 'Session_DB' in locals():
            Session_DB.rollback()
           
        return False
    finally: 
        if 'Session_DB' in locals():
            Session_DB.close()
            
        

#Добавление пользователя Админка

def add_users():
    try:
        # Получаем данные с формы
        first_name_form = request.form['first_name']
        last_name_form = request.form['last_name']
        email_form = request.form['email']
        password_form = request.form['password']
        role_id = 2  # Админ
        is_active = True
        
        # Открываем сессию с БД
        Session_DB = get_db_connection()
        
        # Проверяем, нет ли уже пользователя с таким email
        existing_user = Session_DB.query(User).filter_by(email=email_form).first()
        if existing_user:
            print(f" Пользователь с email {email_form} уже существует")
            return False
        
        # Создаем объект пользователя
        New_User_admin = User(
            email=email_form, 
            password_hash=password_form, 
            first_name=first_name_form, 
            last_name=last_name_form,
            role_id=role_id,
            is_active=is_active
        )
        
        # Добавляем в БД
        Session_DB.add(New_User_admin)
        Session_DB.commit()
        
        print(f" Пользователь {first_name_form} {last_name_form} успешно добавлен")
        return True
   
    except Exception as e:
        print(f" Ошибка при добавлении пользователя: {e}")
        import traceback
        traceback.print_exc()
        if 'Session_DB' in locals():
            Session_DB.rollback()
        return False
    finally:
        if 'Session_DB' in locals():
            Session_DB.close()
 
def delete_product(product_id):
    try:
        Session_DB = get_db_connection ()   # Открываем сессию с Бд для рабьоты с БД
        find_product_DEL = Session_DB.query(Product).filter(Product.id == product_id).first() # ищем продукт который будем удалять по id
        if find_product_DEL: # если не пусто то удаляем
            Session_DB.delete(find_product_DEL)
            Session_DB.commit()
            return True
        else:
            return False
    finally:
        Session_DB.close

