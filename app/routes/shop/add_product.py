from flask import request, jsonify, redirect, url_for
from app import app, db
from flask_login import login_required, current_user
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


@app.route('/add_to_cart_from_single', methods=['POST'])
def add_to_cart_from_single():
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

    return jsonify({'message': 'Товар успешно добавлен в корзину', 'redirect_url': '/cart'})


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