# Импорт необходимых модулей и классов
from flask import jsonify
from flask_login import current_user
from app import app, db
from app.models.cart import Cart


# Обработчик POST-запроса для очистки корзины покупок пользователя
@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    # Получаем идентификатор текущего пользователя
    user_id = current_user.id

    # Получаем список товаров в корзине пользователя
    products = list(Cart.query.filter_by(user_id=user_id).all())

    # Удаляем каждый товар из корзины и сохраняем изменения в базе данных
    for product in products:
        db.session.delete(product)
        db.session.commit()

    # Возвращаем JSON-ответ об успешном удалении товаров из корзины
    return jsonify("Successfully removed")
