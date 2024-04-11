from flask import request, jsonify
from app import app, db
from flask_login import current_user
from app.models.cart import Cart


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    print('spdfmlkisd')
    data = request.get_json()
    product_id = data['product_id']
    user_id = current_user.id

    new_cart = Cart(product_id=product_id, quantity=1, user_id=user_id)
    db.session.add(new_cart)
    db.session.commit()

    return jsonify({'message': 'Товар добавлен в корзину!'})
