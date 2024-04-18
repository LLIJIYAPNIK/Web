# Импорт необходимых модулей и классов
from datetime import datetime
from flask_login import UserMixin
from app import db


# Таблица с пользователями
class User(UserMixin, db.Model):
    __tablename__ = 'users' # Название таблицы

    id = db.Column(db.Integer, primary_key=True) # ID
    mail = db.Column(db.String(100), unique=True, nullable=False) # Почта
    name = db.Column(db.String(100), nullable=False) # Имя
    last_name = db.Column(db.String(100), nullable=False) # Фамилия
    password = db.Column(db.String(100), nullable=False) # Пароль
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # Дата регистрации

    # Метод для получения ID пользователя
    def get_id(self):
        return str(self.id)
