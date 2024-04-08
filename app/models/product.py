from app import db


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    squirrels = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    carbohydrates = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price =db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)