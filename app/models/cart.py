# Импорт необходимых модулей и классов
from app import db


# Таблица пользовательской корзины товаров
class Cart(db.Model):
    __tablename__ = 'cart'  # Название таблицы

    id = db.Column(db.Integer, primary_key=True)  # ID
    quantity = db.Column(db.Integer, nullable=False, default=0)  # Количество
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # ID пользователя
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))  # ID товара

    # Связь с другими таблицами
    user = db.relationship("User", backref="cart")
    product = db.relationship("Product", backref="cart")
