from flask import request, session, flash, redirect, url_for, render_template
from database import get_db_connection
from models import Product,User,Order,UserRole,Basket,OrderItem,OrderStatus
def get_basket_items(user_id):
    try:
        session_DB = get_db_connection()
        query = session_DB.query(Product,Basket.quantity).join(Basket, Product.id == Basket.product_id ).filter(Basket.user_id == user_id).all()
       
        Total_sum = sum(product.price * quantity  for product, quantity in query )
        
        
        return query, Total_sum
    finally:
        session_DB.close()


 
def del_basket_items(user_id, product_id):
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
    except Exception as e:
        print(f"Ошибка при удалении из корзины: {e}")
        return False
    finally:
        session_DB.close()


def create_order_product(user_id, product_id, quantity):
    session_DB = get_db_connection()
    try:
        #  Проверяем наличие товара - ORM
        product = session_DB.query(Product).filter(Product.id == product_id).first()
        
        if not product or product.stock_quantity < quantity:
            return False
        
        #  Получаем order_num - ORM
        last_order = session_DB.query(Basket.order_num)\
            .filter(Basket.user_id == user_id)\
            .order_by(Basket.order_num.desc())\
            .first()
        
        order_number = last_order[0] + 1 if last_order else 1
        
        #  Проверяем есть ли уже товар в корзине - ORM
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
        
        #  Обновляем остатки 
        product.stock_quantity -= quantity
        
        session_DB.commit()
        return True
    finally:
        session_DB.close()
