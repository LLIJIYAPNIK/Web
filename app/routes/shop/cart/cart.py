# Импорт необходимых модулей и классов
from flask import render_template
from flask_login import current_user, login_required
from app import app
from app.models.cart import Cart


# Обработчик GET-запроса для отображения корзины покупок пользователя
@app.route('/cart')
@login_required
def cart():
    # Получаем идентификатор текущего пользователя
    user_id = current_user.id

    # Получаем список товаров в корзине пользователя
    cart = list(Cart.query.filter_by(user_id=user_id).all())

    if cart:
        # Если корзина не пуста, формируем список идентификаторов товаров
        product_ids = [item.product_id for item in cart]

        total = 0

        # Вычисляем общую стоимость товаров в корзине
        for product_index in range(len(cart)):
            total += int(cart[product_index].product.price) * int(cart[product_index].quantity)

        # Отображаем страницу корзины с данными о товарах и общей стоимости
        return render_template("shop/cart.html", product_ids=product_ids, cart=cart, total=total, cart_length=len(cart), life=True)
    else:
        # Если корзина пуста, отображаем страницу корзины без товаров
        return render_template("shop/cart.html", life=False)
