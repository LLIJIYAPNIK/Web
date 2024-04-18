# Импорт необходимых модулей и классов
from flask import jsonify, request
from flask_login import current_user
from app import app, db
from app.models.cart import Cart


# Обработчик POST-запроса для удаления товара из корзины покупок пользователя
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    # Получаем идентификатор текущего пользователя
    user_id = current_user.id

    # Получаем данные JSON-запроса с идентификатором удаляемого товара
    data = request.get_json()
    product_id = int(data['product_id'])

    # Поиск товара в корзине пользователя по идентификатору
    cart_item = Cart.query.filter_by(product_id=product_id, user_id=user_id).first()
    if cart_item:
        # Удаляем товар из корзины и сохраняем изменения в базе данных
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Successfully removed", "product_id": product_id})
    else:
        # Возвращаем сообщение об ошибке, если товар не найден в корзине
        return jsonify({"message": "Item not found in cart"}), 404
