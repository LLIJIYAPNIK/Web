from flask import render_template
from flask_login import current_user, login_required
from app import app
from app.models.cart import Cart


@app.route('/cart')
@login_required
def cart():
    user_id = current_user.id

    cart = list(Cart.query.filter_by(user_id=user_id).all())

    if cart:
        product_ids = [item.product_id for item in cart]

        total = 0

        for product_index in range(len(cart)):
            print(cart[product_index].product.price, cart[product_index].quantity)
            total += int(cart[product_index].product.price) * int(cart[product_index].quantity)
        print(total)

        return render_template("shop/cart.html", product_ids=product_ids, cart=cart, total=total, cart_length=len(cart), life=True)
    else:
        return render_template("shop/cart.html", life=False)