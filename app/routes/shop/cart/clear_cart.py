from flask import jsonify
from flask_login import current_user
from app import app, db
from app.models.cart import Cart


@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    user_id = current_user.id

    products = list(Cart.query.filter_by(user_id=user_id).all())

    for product in products:
        db.session.delete(product)
        db.session.commit()

    return jsonify("Successfully removed")