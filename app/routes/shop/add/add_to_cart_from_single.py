# Импорт необходимых модулей и классов
from flask import request, jsonify
from app import app, db
from app.models.cart import Cart


# Обработчик POST-запроса для добавления товара в корзину с указанием количества товара
@app.route('/add_to_cart_from_single', methods=['POST'])
def add_to_cart_from_single():
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

    # Возвращаем JSON-ответ с сообщением о добавлении товара и URL для перенаправления на страницу корзины
    return jsonify({'message': 'Товар успешно добавлен в корзину', 'redirect_url': '/cart'})
