from models import Gyms
from geopy.distance import geodesic
from functools import lru_cache


def get_gyms(user_x, user_y, db):
    @lru_cache(maxsize=100)
    def get_distance(start_x, start_y, gym):
        return geodesic((start_x, start_y), (gym.x, gym.y)).m  # Извлечение значений координат

    # Запрос для поиска ближайших мест
    results = db.session.query(Gyms).all()  # Извлекаем все объекты Gyms

    results.sort(key=lambda gym: get_distance(user_x, user_y, gym))  # Сортируем по расстоянию

    gyms = []

    for gym in results:
        gyms.append([gym.title, gym.adress, round(get_distance(user_x, user_y, gym)), gym.x, gym.y])

    return gyms[0:3]
