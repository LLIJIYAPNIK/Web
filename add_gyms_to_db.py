import time
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Gyms

# API ключ
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

# JSON-строка
json_data = [
    'World Class'
]

time.sleep(0.1)

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
        if 'Моск' in result['properties']['description']:
            s = f"Название: {result['properties']['name']} {result['properties']['description']} "
            response_coord = requests.get(
                f"https://geocode-maps.yandex.ru/1.x/?apikey=978bc106-09fd-4aa3-b6bd-40c122f310ea&geocode={result['properties']['description']}&format=json")
            data_coord = response_coord.json()
            for feature_member in data_coord['response']['GeoObjectCollection']['featureMember']:
                # Теперь вы можете получить доступ к полям внутри feature_member
                coords = [float(coord) for coord in str(feature_member['GeoObject']['Point']['pos']).split()[::-1]]
            print(s)
            engine = create_engine('mysql+mysqlconnector://Sasha:Sasha@localhost/mydb')
            Base.metadata.create_all(engine)

            # Создаем сеанс
            Session = sessionmaker(bind=engine)
            session = Session()

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
