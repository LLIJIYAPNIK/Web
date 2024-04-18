# Импорт необходимых модулей и классов
from app.models.gym import Gyms
from geopy.distance import geodesic
from functools import lru_cache


def get_gyms(user_x, user_y, db):
    @lru_cache(maxsize=100)  # Декоратор для кэширования результатов функции
    def get_distance(start_x, start_y, gym):
        return geodesic((start_x, start_y), (gym.x, gym.y)).m  # Расчет расстояния между точками

    # Запрос для получения всех объектов Gyms из базы данных
    results = db.session.query(Gyms).all()

    results.sort(key=lambda gym: get_distance(user_x, user_y, gym))  # Сортировка результатов по расстоянию

    gyms = []

    for gym in results:
        gyms.append([gym.title, gym.adress, round(get_distance(user_x, user_y, gym)), gym.x, gym.y])

    return gyms[0:3]  # Возвращаем три ближайших зала фитнеса
