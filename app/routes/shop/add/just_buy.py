from app import app
from flask import request, jsonify
from app import db
from app.models.cart import Cart


@app.route('/just_buy', methods=['POST'])
def just_buy():
    data = request.get_json()
    user_id = int(data['user_id'])
    product_id = int(data['product_id'])
    quantity = int(data['quantity'])

    cart = Cart.query.filter_by(product_id=product_id, user_id=user_id).first()

    if cart is None:
        new_cart = Cart(product_id=product_id, user_id=user_id, quantity=quantity)
        db.session.add(new_cart)
    else:
        cart.quantity = quantity
    db.session.commit()

    return jsonify({'message': 'Success'})