# Импорт необходимых модулей и классов
from app import db


# Таблица с реакциями пользователей
class PostReactions(db.Model):
    __tablename__ = 'post_reactions'  # Название статьи

    id = db.Column(db.Integer, primary_key=True)  # ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ID пользователя
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)  # ID статьи
    reaction_type = db.Column(db.String(10), nullable=False)  # Тип реакции 'like'/'dislike'/'None'

    # Связь с другими таблицами
    user = db.relationship("User", backref="post_reactions")
    post = db.relationship("Posts", backref="post_reactions")
