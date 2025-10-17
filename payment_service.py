from datetime import datetime

def process_order(user_id, total_amount, payment_method, card_data=None):
    """Основная функция обработки заказа"""
    try:
        print(f"Обработка заказа для пользователя {user_id}")
        print(f"Сумма: {total_amount}, Метод оплаты: {payment_method}")
        
        # Создаем заказ в БД
        success, order_number = create_order_in_db(user_id, total_amount, payment_method)
        
        if not success:
            error_msg = f"Ошибка создания заказа: {order_number}"
            print(f"ОШИБКА: {error_msg}")
            return False, None, error_msg
        
        print(f"Заказ создан: {order_number}")
        
        # Обрабатываем платеж
        payment_success, payment_message = process_payment(payment_method, card_data)
        
        if not payment_success:
            error_msg = f"Ошибка оплаты: {payment_message}"
            print(f"ОШИБКА: {error_msg}")
            return False, None, error_msg
        
        # Очищаем корзину
        try:
            from basket import del_basket_items, get_basket_items
            
            basket_items, total, total_quantity = get_basket_items(user_id)
            print(f"Очистка корзины: {len(basket_items)} товаров")
            
            for item in basket_items:
                product = item[0]
                del_basket_items(user_id, product.id)
                print(f"Удален товар {product.id} из корзины")
                
        except Exception as e:
            print(f"Ошибка при очистке корзины: {str(e)}")
        
        success_msg = f"Заказ {order_number} успешно создан! {payment_message}"
        print(f"УСПЕХ: {success_msg}")
        return True, order_number, success_msg
        
    except Exception as e:
        error_msg = f"Ошибка при обработке заказа: {str(e)}"
        print(f"ОШИБКА: {error_msg}")
        return False, None, error_msg

def create_order_in_db(user_id, total_amount, payment_method):
    """Создаем заказ в БД"""
    try:
        from database import get_db_connection
        from models import Order, OrderStatus, OrderItem, Basket, Product, Payment
        
        session_DB = get_db_connection()
        
        # Получаем статус "новый - в бд добавил" 
        new_status = session_DB.query(OrderStatus).filter_by(status="новый").first()
        
        if not new_status:
            session_DB.close()
            return False, "Статус 'новый' не найден"
        
        # Создаем заказ
        new_order = Order(
            user_id=user_id,
            order_status_id=new_status.id,
            total_amount=total_amount,
            shipping_address="Адрес доставки",
            billing_address="Адрес оплаты",
            customer_notes="",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        session_DB.add(new_order)
        session_DB.flush()
        
        # Номер заказа
        order_number = f"ORD-{new_order.id}"
        
        # Добавляем товары из корзины
        basket_items = session_DB.query(Basket).filter_by(user_id=user_id).all()
        
        for basket_item in basket_items:
            product = session_DB.query(Product).filter_by(id=basket_item.product_id).first()
            if product:
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=basket_item.product_id,
                    quantity=basket_item.quantity,
                    unit_price=product.price
                )
                session_DB.add(order_item)
        
        # Создаем платеж
        payment = Payment(
            order_id=new_order.id,
            payment_method=payment_method,
            amount=total_amount,
            status="completed",
            transaction_id=f"TXN-{int(datetime.now().timestamp())}",
            created_at=datetime.now()
        )
        session_DB.add(payment)
        
        # Очищаем корзину
        session_DB.query(Basket).filter_by(user_id=user_id).delete()
        
        # Сохраняем в БД
        session_DB.commit()
        session_DB.close()
        
        return True, order_number
        
    except Exception as e:
        if 'session_DB' in locals():
            session_DB.rollback()
            session_DB.close()
        return False, str(e)

def process_payment(payment_method, card_data=None):
    """Обрабатывает платеж"""
    try:
        if payment_method == 'card':
            if not card_data:
                return False, "Данные карты не предоставлены"
            
            
            if validate_card(card_data):
                return True, "Оплата картой прошла успешно"
            else:
                return False, "Ошибка оплаты картой"
        else:
            
            return True, "Ожидание оплаты наличными при получении"
            
    except Exception as e:
        return False, f"Ошибка при обработке платежа: {str(e)}"

def validate_card(card_data):
    """Проверка карты"""
    try:
        card_number = card_data.get('card_number', '').replace(' ', '')
        expiry_date = card_data.get('expiry_date', '')
        cvv = card_data.get('cvv', '')
        card_holder = card_data.get('card_holder', '')
        
        # не важно чем заполняем
        if not all([card_number, expiry_date, cvv, card_holder]):
            return False
        
        # любые данные.
        return True
        
    except Exception:
        return False