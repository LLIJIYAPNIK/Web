import time
import requests
import json

# API ключ
api_key = "8a0e4f5f-f02b-4a50-827b-f4f417184124"

# JSON-строка
json_data = [
    'Fitness USSR'
]

# Закодированная JSON-строка
encoded_data = json.dumps(json_data)

# Параметры запроса
params = {
    "apikey": api_key,
    "text": encoded_data,
    'results': 100,
    "lang": "ru"
}

# Отправка запроса к API
response = requests.get("https://search-maps.yandex.ru/v1/", params=params)
print(response.text)

# Проверка ответа
if response.status_code == 200:
    # Преобразование ответа в JSON
    data = response.json()

    # Получение информации о результатах
    results = data["features"]
    # Вывод информации о результатах
    for result in results:
        if 'Москва' in result['properties']['description']:
            s = f"Название: {result['properties']['name']} {result['properties']['description']} "
            response_coord = requests.get(
                f"https://geocode-maps.yandex.ru/1.x/?apikey=978bc106-09fd-4aa3-b6bd-40c122f310ea&geocode={result['properties']['description']}&format=json")
            data_coord = response_coord.json()
            for feature_member in data_coord['response']['GeoObjectCollection']['featureMember']:
                # Теперь вы можете получить доступ к полям внутри feature_member
                coords = [float(coord) for coord in str(feature_member['GeoObject']['Point']['pos']).split()[::-1]]
            print(s)
            from models import *

            engine = create_engine('sqlite:///database.sqlite')

            # Создаем таблицу, если она не существует
            Base.metadata.create_all(engine)

            # Создаем сеанс
            session = sessionmaker(bind=engine)()

            # Добавляем пользователя
            user = Gyms(title=f"{result['properties']['name']}", adress=f"{result['properties']['description']}",
                        x=coords[0], y=coords[1])
            session.add(user)

            # Сохраняем изменения
            session.commit()

            # Закрываем сеанс
            session.close()

            time.sleep(0.1)


else:
    # Ошибка при запросе к API
    print(f"Ошибка: {response.status_code}")
