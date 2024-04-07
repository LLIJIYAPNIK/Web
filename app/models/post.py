from datetime import datetime
from app import db


class Posts(db.Model):
    __tablename__ = 'posts'
    __searchable__ = ['title', 'content']

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)

    user = db.relationship("User", backref="posts")