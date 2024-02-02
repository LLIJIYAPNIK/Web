from sqlalchemy import create_engine, Column, Integer, String, Float

from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Gyms(Base):
    __tablename__ = 'gyms'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=False)
    adress = Column(String(80), unique=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)


engine = create_engine('sqlite:///database.sqlite')

# Создаем таблицу, если она не существует
Base.metadata.create_all(engine)

