from flask import Flask, render_template
from app.models.product import Product
from app import app


@app.route('/shop')
def shop():
    products = Product.query.all()
    return render_template('shop1.html', products=products)
