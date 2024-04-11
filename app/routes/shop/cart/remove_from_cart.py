from flask import jsonify, request
from flask_login import current_user
from app import app, db
from app.models.cart import Cart


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    user_id = current_user.id

    data = request.get_json()
    product_id = int(data['product_id'])

    cart_item = Cart.query.filter_by(product_id=product_id, user_id=user_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Successfully removed", "product_id": product_id})
    else:
        return jsonify({"message": "Item not found in cart"}), 404