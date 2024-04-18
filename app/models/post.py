# Импорт необходимых модулей и классов
from datetime import datetime
from app import db


# Таблица с постами пользователей
class Posts(db.Model):
    __tablename__ = 'posts'  # Название таблицы
    __searchable__ = ['title', 'content']  # В каких данных искать совпадения поиску

    id = db.Column(db.Integer, primary_key=True)  # ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ID пользователя
    title = db.Column(db.String(100), nullable=False)  # Название статьи
    content = db.Column(db.Text, nullable=False)  # Контент статьи
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата создания статьи
    is_published = db.Column(db.Boolean, default=False)  # Опубликована ли статьи (T/F)

    # Связь с другими таблицами
    user = db.relationship("User", backref="posts")
