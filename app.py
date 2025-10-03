from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'# без этого проблема с сессиями

# из созданных
from database import init_db
from auth import login_user, register_user, logout_user
from products import get_products, get_product, create_order_product, get_basket_items
from admin import admin_panel, add_product, delete_product

# Главная страница
@app.route('/')
def index():
    search = request.args.get('search', '')
    min_price = request.args.get('min_price', '')
    max_price = request.args.get('max_price', '')
    
    products = get_products(search, min_price, max_price)
    return render_template('index.html', products=products, search=search, min_price=min_price, max_price=max_price)

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
        flash('Товар в корзине!', 'success')
    else:
        flash('Недостаточно товара', 'error')
    
    return redirect(url_for('index'))

# Админ панель
@app.route('/admin')
def admin():
    if not session.get('role_id'):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('index'))
    
    users = admin_panel()
    return render_template('admin.html',users=users)

# Добавление товара (админ) НеДОДЕЛАНО
@app.route('/add_product', methods=['POST'])
def add_product():
    if not session.get('admin'):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('index'))
    
    if add_product():
        flash('Товар успешно добавлен!', 'success')
    else:
        flash('Ошибка добавления', 'error')
    
    return redirect(url_for('admin'))

# Удаление товара (админ) НЕ ДОДЕЛАНО
@app.route('/delete_product/<int:product_id>')
def delete_product_route(product_id):
    if not session.get('admin'):
        flash('Доступ запрещен', 'error')
        return redirect(url_for('index'))
    
    if delete_product(product_id):
        flash('Товар удален!', 'success')
    else:
        flash('Ошибка удаления', 'error')
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)