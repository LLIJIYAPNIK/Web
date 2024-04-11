from flask import Flask, render_template
from flask_login import current_user
from app.models.cart import Cart
from app.models.product import Product
from app import app


@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    cart = Cart.query.filter_by(user_id=current_user.id).all()
    product_ids = [item.product_id for item in cart]
    quantity = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if quantity == None:
        return render_template("shop/shop-single.html", product=product, cart=product_ids, user=current_user.id)
    else:
        return render_template("shop/shop-single.html", product=product, cart=product_ids, quantity=quantity.quantity,
                               user=current_user.id)
