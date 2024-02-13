from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Gyms(Base):
    __tablename__ = 'gyms'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=False)
    adress = Column(String(80), unique=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    last_name = Column(String(50), unique=False)
    mail = Column(String(50), unique=True)
    password = Column(String(80), unique=False)

    def __init__(self, name, last_name, mail, password):
        self.name = name
        self.last_name = last_name
        self.mail = mail
        self.password = password


