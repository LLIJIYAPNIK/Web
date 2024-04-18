# Импорт необходимых модулей и классов
from app import db


# Таблица с предоставляемыми товарами
class Product(db.Model):
    __tablename__ = 'product'  # Название товара

    id = db.Column(db.Integer, primary_key=True)  # ID
    name = db.Column(db.String(100), nullable=False)  # Название товара
    calories = db.Column(db.Integer, nullable=False)  # Калории
    squirrels = db.Column(db.Integer, nullable=False)  # Белки
    fats = db.Column(db.Integer, nullable=False)  # Жиры
    carbohydrates = db.Column(db.Integer, nullable=False)  # Углеводы
    description = db.Column(db.Text, nullable=False)  # Описание
    price = db.Column(db.Integer, nullable=False)  # Цена
    image = db.Column(db.String(100), nullable=False)  # Путь к изображению
