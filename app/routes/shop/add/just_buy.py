# Импорт необходимых модулей и классов
from flask import request, jsonify
from app import app, db
from app.models.cart import Cart


# Обработчик POST-запроса для покупки товара без добавления в корзину
@app.route('/just_buy', methods=['POST'])
def just_buy():
    # Получаем данные из JSON-запроса
    data = request.get_json()
    user_id = int(data['user_id'])
    product_id = int(data['product_id'])
    quantity = int(data['quantity'])

    # Проверяем, есть ли товар уже в корзине пользователя
    cart = Cart.query.filter_by(product_id=product_id, user_id=user_id).first()

    if cart is None:
        # Если товара нет в корзине, создаем новую запись
        new_cart = Cart(product_id=product_id, user_id=user_id, quantity=quantity)
        db.session.add(new_cart)
    else:
        # Если товар уже есть в корзине, обновляем количество
        cart.quantity = quantity

    # Сохраняем изменения в базе данных
    db.session.commit()

    # Возвращаем JSON-ответ с сообщением об успешной покупке
    return jsonify({'message': 'Success'})
