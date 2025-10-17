

from database import get_db_connection
from models.user import User
from models.product import Product
from sqlalchemy import or_

def get_products(search='', min_price='', max_price=''): # Получение всех проудктов для магазина страницы товаров
    Session_DB = get_db_connection()
    
    try:
        # Начинаем запрос
       
        query = Session_DB.query(Product).filter(Product.is_active == True)
        # Добавляем условия фильтрации
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.description.ilike(f'%{search}%')
                )
            )
        
        
        if min_price:
            query = query.filter(Product.price >= float(min_price))
        
        if max_price:
            query = query.filter(Product.price <= float(max_price))
        
        # Сортировка и выполнение запроса
        products = query.order_by(Product.id.desc()).all()
        
        return products
        
    except Exception as e:
        print(f"Ошибка при получении продуктов: {e}")
        return []
    finally:
        Session_DB.close()


def get_product(product_id): # Получение одного продукта
    try:
        Session_BD = get_db_connection()
        query = Session_BD.query(Product).filter(
            Product.id == product_id, 
            Product.is_active == True  
        ).first()
        if query:
        
            return query
        else:
            return None
    finally:
        Session_BD.close()     






