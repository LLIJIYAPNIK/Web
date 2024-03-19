from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.Model


class Gyms(Base):
    __tablename__ = 'gyms'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False)
    adress = db.Column(db.String(80), unique=False)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)


class User(UserMixin, Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return str(self.id)


class Posts(Base):
    __tablename__ = 'posts'
    __searchable__ = ['title', 'content']

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref="posts")


class PostReactions(Base):
    __tablename__ = 'post_reactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    reaction_type = db.Column(db.String(10), nullable=False)  # 'like' or 'dislike'

    user = db.relationship("User", backref="post_reactions")
    post = db.relationship("Posts", backref="post_reactions")
