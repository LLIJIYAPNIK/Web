from models import *
from geopy.distance import geodesic
from functools import lru_cache
from sqlalchemy.sql import literal_column  # Импорт функции literal_column


def get_gyms(user_x, user_y):
    @lru_cache(maxsize=100)
    def get_distance(start_x, start_y, gym):
        return geodesic((start_x, start_y), (gym.x, gym.y)).m  # Извлечение значений координат

    session = sessionmaker(bind=engine)()

    # Запрос для поиска ближайших мест
    results = session.query(Gyms).order_by(
        literal_column("1").asc()  # Временная заглушка
    ).all()  # Извлекаем все объекты Gyms

    results.sort(key=lambda gym: get_distance(user_x, user_y, gym))  # Сортируем по расстоянию

    gyms = []

    for gym in results:
        gyms.append([gym.title, gym.adress, round(get_distance(user_x, user_y, gym)), gym.x, gym.y])

    return gyms[0:3]

    session.close()
