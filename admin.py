from flask import request, session
from database import get_db_connection
from models import User, Product
from sqlalchemy import Time
from sqlalchemy.exc import SQLAlchemyError

def admin_panel():
    try:
        Session_DB = get_db_connection()
        admins = Session_DB.query(User).filter(User.role_id == 2).all()
        return admins
    except SQLAlchemyError as e:
        print(f"Ошибка при получении списка админов: {e}")
        return []
    finally:
        if Session_DB:
            Session_DB.close()

# Добавление товара в Админке
def add_products():
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

    Session_DB = None
    try:
        Session_DB = get_db_connection()
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
        
        Session_DB.add(new_product)
        Session_DB.commit()
        return True
        
    except SQLAlchemyError as e:
        if Session_DB:
            Session_DB.rollback()
        print(f"Ошибка при добавлении товара: {e}")
        return False
    finally: 
        if Session_DB:
            Session_DB.close()

# Добавление пользователя Админка
def add_users():
    # Получаем данные с формы
    first_name_form = request.form['first_name']
    last_name_form = request.form['last_name']
    email_form = request.form['email']
    password_form = request.form['password']
    role_id = 2  # Админ
    is_active = True
    
    Session_DB = None
    try:
        Session_DB = get_db_connection()
        
        # Проверяем, нет ли уже пользователя с таким email
        existing_user = Session_DB.query(User).filter_by(email=email_form).first()
        if existing_user:
            print(f"Пользователь с email {email_form} уже существует")
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
        
        Session_DB.add(New_User_admin)
        Session_DB.commit()
        
        print(f"Пользователь {first_name_form} {last_name_form} успешно добавлен")
        return True

    except SQLAlchemyError as e:
        print(f"Ошибка БД при добавлении пользователя: {e}")
        if Session_DB:
            Session_DB.rollback()
        return False
    finally:
        if Session_DB:
            Session_DB.close()

def delete_product(product_id):
    Session_DB = None
    try:
        Session_DB = get_db_connection()
        find_product_DEL = Session_DB.query(Product).filter(Product.id == product_id).first()
        if find_product_DEL:
            Session_DB.delete(find_product_DEL)
            Session_DB.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        print(f"Ошибка БД при удалении продукта: {e}")
        if Session_DB:
            Session_DB.rollback()
        return False
    finally:
        if Session_DB:
            Session_DB.close()