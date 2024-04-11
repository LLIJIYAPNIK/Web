from flask import Flask, render_template
from flask_login import current_user
from app.models.cart import Cart
from app.models.product import Product
from app import app


@app.route('/shop')
def shop():
    products = Product.query.all()
    cart = Cart.query.filter_by(user_id=current_user.id).all()
    product_ids = [item.product_id for item in cart]
    return render_template('shop/shop1.html', products=products, cart=product_ids)
