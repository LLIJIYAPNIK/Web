from app import db


class Gyms(db.Model):
    __tablename__ = 'gyms'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False)
    adress = db.Column(db.String(80), unique=False)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)