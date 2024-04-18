# Импорт необходимых модулей и классов
from flask import request, jsonify
from app import app, db
from flask_login import current_user
from app.models.cart import Cart


# Создаем маршрут для обработки POST-запросов на добавление товара в корзину
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Получаем данные о товаре из JSON-запроса
    data = request.get_json()
    product_id = data['product_id']
    user_id = current_user.id

    # Создаем новую запись в корзине с данными о товаре и пользователе
    new_cart = Cart(product_id=product_id, quantity=1,
                    user_id=user_id)

    # Сохраняем изменения в базе данных
    db.session.add(new_cart)
    db.session.commit()

    return jsonify({
        'message': 'Товар добавлен в корзину!'})
