# Импорт необходимых модулей и классов
from app import db


# Таблица фитнес-клубов
class Gyms(db.Model):
    __tablename__ = 'gyms'  # Название таблицы

    id = db.Column(db.Integer, primary_key=True)  # ID
    title = db.Column(db.String(50), unique=False)  # Название
    adress = db.Column(db.String(80), unique=False)  # Адрес
    x = db.Column(db.Float, nullable=False)  # Координата X - lon
    y = db.Column(db.Float, nullable=False)  # Координата Y - lat
