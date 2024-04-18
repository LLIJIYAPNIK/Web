# Импорт необходимых модулей и классов
from flask import render_template
from flask_login import current_user, login_required
from app.models.cart import Cart
from app.models.product import Product
from app import app


# Обработчик GET-запроса для страницы товара
@app.route('/product/<int:product_id>')
@login_required
def product(product_id):
    # Получаем информацию о товаре по его идентификатору из базы данных
    product = Product.query.filter(Product.id == product_id).first()

    # Получаем все товары в корзине текущего пользователя
    cart = Cart.query.filter_by(user_id=current_user.id).all()

    # Формируем список идентификаторов товаров в корзине
    product_ids = [item.product_id for item in cart]

    # Получаем количество конкретного товара в корзине текущего пользователя
    quantity = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    # Проверяем наличие количества товара в корзине
    if quantity is None:
        return render_template("shop/shop-single.html", product=product, cart=product_ids, user=current_user.id)
    else:
        return render_template("shop/shop-single.html", product=product, cart=product_ids, quantity=quantity.quantity,
                               user=current_user.id)
