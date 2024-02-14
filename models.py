from sqlalchemy import Column, Integer, String, Float
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.Model

class Gyms(Base):
    __tablename__ = 'gyms'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False)
    address = db.Column(db.String(80), unique=False)
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
