from flask import Flask, render_template
from app.models.product import Product
from app import app


@app.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    return render_template("product.html", product=product)