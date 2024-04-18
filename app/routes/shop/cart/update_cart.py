# Импорт необходимых модулей и классов
from flask import jsonify, request
from flask_login import current_user
from app import app, db
from app.models.cart import Cart


# Обработчик POST-запроса для обновления корзины покупок пользователя
@app.route('/update_cart', methods=['POST'])
def update_cart():
    # Получаем идентификатор текущего пользователя
    user_id = current_user.id

    # Получаем данные JSON-запроса с идентификатором товара и его количеством
    data = request.get_json()
    product_id = int(data['product_id'])
    quantity = int(data['quantity'])

    # Находим товар в корзине пользователя по идентификатору и обновляем его количество
    cart_now = Cart.query.filter_by(product_id=product_id, user_id=user_id).first()
    cart_now.quantity = quantity
    db.session.commit()

    # Вычисляем общую стоимость для обновленного товара
    total_for_product = cart_now.quantity * cart_now.product.price

    # Получаем список всех товаров в корзине пользователя
    cart = list(Cart.query.filter_by(user_id=user_id).all())

    # Вычисляем общую стоимость всех товаров в корзине
    total = 0
    for product_index in range(len(cart)):
        total += int(cart[product_index].product.price) * int(cart[product_index].quantity)

    # Формируем ответ с общей стоимостью и стоимостью обновленного товара
    response = {
        "total": total,
        "total_for_product": total_for_product
    }

    return jsonify(response)
