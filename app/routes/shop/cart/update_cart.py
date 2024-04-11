from flask import jsonify, request
from flask_login import current_user
from app import app, db
from app.models.cart import Cart


@app.route("/update_cart", methods=["POST"])
def update_cart():
    user_id = current_user.id

    data = request.get_json()
    print(data)
    product_id = int(data['product_id'])
    quantity = int(data['quantity'])

    cart_now = Cart.query.filter_by(product_id=product_id, user_id=user_id).first()
    cart_now.quantity = quantity
    db.session.commit()

    total_for_product = cart_now.quantity * cart_now.product.price

    cart = list(Cart.query.filter_by(user_id=user_id).all())

    total = 0

    for product_index in range(len(cart)):
        total += int(cart[product_index].product.price) * int(cart[product_index].quantity)

    response = {
        "total": total,
        "total_for_product": total_for_product
    }

    return jsonify(response)