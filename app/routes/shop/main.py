# Импорт необходимых модулей и классов
from flask import render_template
from flask_login import current_user, login_required
from app.models.cart import Cart
from app.models.product import Product
from app import app


# Обработчик GET-запроса для страницы магазина
@app.route('/shop')
@login_required
def shop():
    # Получаем все товары из базы данных
    products = Product.query.all()

    # Получаем все товары в корзине текущего пользователя
    cart = Cart.query.filter_by(user_id=current_user.id).all()

    # Формируем список идентификаторов товаров в корзине
    product_ids = [item.product_id for item in cart]

    # Отображаем шаблон страницы магазина с товарами и идентификаторами товаров в корзине
    return render_template('shop/shop1.html', products=products, cart=product_ids)
