from flask import request, session, flash, redirect, url_for, render_template
from database import get_db_connection
from models import Product,User,Order,UserRole,Basket,OrderItem,OrderStatus
from sqlalchemy.exc import SQLAlchemyError

def get_basket_items(user_id):
    session_DB = None
    try:
        session_DB = get_db_connection()
        query = session_DB.query(Product,Basket.quantity).join(Basket, Product.id == Basket.product_id ).filter(Basket.user_id == user_id).all()
       
        Total_sum = sum(product.price * quantity  for product, quantity in query )
<<<<<<< Updated upstream
        total_quantity = sum(quantity for product, quantity in query)  # ← общее количество
        
        return query, Total_sum, total_quantity
=======
        total_quantity = sum(quantity for product, quantity in query)
        
        return query, Total_sum, total_quantity
    except SQLAlchemyError as e:
        print(f"Ошибка БД при получении корзины: {e}")
        return [], 0, 0
>>>>>>> Stashed changes
    finally:
        if session_DB:
            session_DB.close()



 
def del_basket_items(user_id, product_id):
    session_DB = None
    try:
        session_DB = get_db_connection()
        query = session_DB.query(Basket).filter(
            Basket.user_id == user_id, 
            Basket.product_id == product_id
        ).first()
        
        if query:
            session_DB.delete(query)
            session_DB.commit()
            return True
        else:
            return False
    except SQLAlchemyError as e:
        print(f"Ошибка БД при удалении из корзины: {e}")
        if session_DB:
            session_DB.rollback()
        return False
    finally:
        if session_DB:
            session_DB.close()


def create_order_product(user_id, product_id, quantity):
    session_DB = None
    try:
        session_DB = get_db_connection()
        
        # Проверяем наличие товара
        product = session_DB.query(Product).filter(Product.id == product_id).first()
        
        if not product or product.stock_quantity < quantity:
            return False
        
        # Получаем order_num
        last_order = session_DB.query(Basket.order_num)\
            .filter(Basket.user_id == user_id)\
            .order_by(Basket.order_num.desc())\
            .first()
        
        order_number = last_order[0] + 1 if last_order else 1
        
        # Проверяем есть ли уже товар в корзине
        existing_item = session_DB.query(Basket)\
            .filter(
                Basket.user_id == user_id,
                Basket.product_id == product_id
            )\
            .first()
        
        if existing_item:
            existing_item.quantity += quantity
        else:
            basket_item = Basket(
                user_id=user_id,
                product_id=product_id,
                quantity=quantity,
                order_num=order_number
            )
            session_DB.add(basket_item)
        
        # Обновляем остатки
        product.stock_quantity -= quantity
        
        session_DB.commit()
        return True
    except SQLAlchemyError as e:
        print(f"Ошибка БД при создании заказа: {e}")
        if session_DB:
            session_DB.rollback()
        return False
    finally:
        if session_DB:
            session_DB.close()
