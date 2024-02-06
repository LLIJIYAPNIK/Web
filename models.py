from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Gyms(Base):
    __tablename__ = 'gyms'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=False)
    adress = Column(String(80), unique=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)

# Укажите параметры подключения к вашей базе данных MySQL
# Замените 'mysql+mysqlconnector://username:password@hostname/dbname' на свои реальные данные
engine = create_engine('mysql+mysqlconnector://Sasha:Sasha@localhost/mydb')

# Создаем таблицу, если она не существует
Base.metadata.create_all(engine)
