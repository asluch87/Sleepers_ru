from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'# без этого проблема с сессиями

from models.product import Product
from database import get_db_connection

# из созданных
#from database import init_db
from auth import login_user, register_user, logout_user,edit_profil_users,get_user_by_id
from products import get_products, get_product
from admin import admin_panel, add_products, delete_product ,add_users
from basket import  create_order_product, get_basket_items,del_basket_items
from models import User

# Главная страница
@app.route('/')
def index():
    search = request.args.get('search', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    message = request.args.get('message')
    
    products = get_products(search, min_price, max_price)
    return render_template('index.html', products=products, search=search, 
                         min_price=min_price, max_price=max_price, message=message)

# Страница товара
@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product(product_id)
    if not product:
        flash('Товар не найден', 'error')
        return redirect(url_for('index'))
    return render_template('product_detail.html', product=product)

# Логин
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return login_user()
    return render_template('login.html')

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return register_user()
    return render_template('register.html')

# Выход
@app.route('/logout')
def logout():
    return logout_user()

# Корзина
@app.route('/inbox')
def inbox():
    if 'id' not in session:
        flash('Войдите в систему', 'error')
        return redirect(url_for('login'))
    
    basket_items, total = get_basket_items(session['id'])
    return render_template('inbox.html', basket_items=basket_items, total=total)
 
# Создание заказа
@app.route('/create_order/<int:product_id>', methods=['POST'])
def create_order_route(product_id):
    if 'id' not in session:
        flash('Войдите в систему чтобы сделать заказ', 'error')
        return redirect(url_for('login'))
    
    quantity = int(request.form['quantity'])
    result = create_order_product(session['id'], product_id, quantity)
    
    if result:
            message = "Товар добавлен в корзину"
    else:
            message = "Товар не может быть добавлен в корзину"
    
    return redirect(request.referrer or url_for('index'))

# Админ панель
@app.route('/admin')
def admin():
    if not session.get('role_id'):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('index'))
    
    users = admin_panel()
    return render_template('admin.html',users=users)

# Добавление товара (админ) 
@app.route('/add_product', methods=['POST'])
def add_product():
    if session.get('role_id') != 2 :
        flash('Доступ запрещен', 'error')
        return redirect(url_for('index'))
    
    result = add_products()
    
    if result:
        flash('Товар успешно добавлен!', 'success')
        
    else:
        flash('Ошибка при добавлении товара', 'error')
    
    return redirect(url_for('admin'))

# Добавление Пользователя (админ) НеДОДЕЛАНО
@app.route('/add_user', methods=['POST'])
def add_user():
    if session.get('role_id') != 2:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('index'))
    
    new_user_admin = add_users()
    
    return redirect(url_for('admin'))






# Удаление для Админа не доделано
@app.route('/delete_basket/<int:product_id>', methods=['GET', 'POST'])
def delete_product_basket(product_id):  # Убрал параметр id

 
    if session.get('role_id') == 1:
        flash("ERROR", "error")
        return redirect(url_for('index'))
    


    if del_basket_items(session.get('id'), product_id):
        flash("Товар успешно удален")
    else:
        flash("Товар не удален")
    
    return redirect(url_for('admin'))

# Редактирование профля
@app.route("/edit_profil", methods=['GET','POST'])
def edit_profil():
    if request.method == 'POST':
        if edit_profil_users():
            message = "Профиль успешно обновлен"
        else:
            message = "Не успешно"
        return redirect(f'/edit_profil?message={message}')
    
    # GET запрос
    message = request.args.get('message')
    from auth import get_user_by_id
    user = get_user_by_id(session['id'])
    return render_template('edit_profil.html', user=user, message=message)


#Удаление профиля

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    from auth import delete_user_profile  # импортируем функцию
    
    if delete_user_profile(user_id):
        return redirect(url_for('index'))  # после удаления на главную
    else:
        return redirect(url_for('edit_profil'))  # при ошибке обратно в редактирование





#Оплата и доставка
@app.route('/delivery_Payment',methods = ['GET','POST'])
def delivery_Payment():
 return render_template('delivery_Payment.html')  




#удаление из корзины покупателем.
@app.route('/delete_from_basket/<int:product_id>', methods=['POST'])
def delete_from_basket(product_id):
    if 'id' not in session:
        flash('Войдите в систему', 'error')
        return redirect(url_for('login'))
    
    del_basket_items(session['id'], product_id)
    return redirect(url_for('inbox'))  # Просто возвращаем в корзину

@app.route('/delete_from_basket/<int:product_id>', methods=['POST'])



@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if session.get('role_id') != 2:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Обработка формы редактирования
        result = edit_profil_users(user_id)
        if result:
            flash('Пользователь успешно обновлен!', 'success')
            return redirect(url_for('admin'))
        else:
            # Остаемся на странице редактирования с ошибкой
            return redirect(url_for('edit_user', user_id=user_id))
    
    # GET запрос - показываем форму редактирования
    Session_DB = get_db_connection()
    try:
        user = Session_DB.query(User).filter(User.id == user_id).first()
        if not user:
            flash('Пользователь не найден', 'error')
            return redirect(url_for('admin'))
        
        return render_template('edit_user.html', user=user)
    finally:
        Session_DB.close()


if __name__ == '__main__':
   # init_db()
    app.run(debug=True)



        