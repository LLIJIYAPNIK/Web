# Импорт необходимых модулей и классов
from app import app, db
from app.get_nearst_gym import get_gyms
from flask import render_template, request, redirect

latitude_user = 0
longitude_user = 0


# Обработчик POST-запроса для получения координат пользователя
@app.route("/get_location", methods=["POST"])
def get_location():
    global latitude_user, longitude_user
    data = request.get_json()
    latitude = data["latitude"]
    longitude = data["longitude"]
    print(f"Latitude: {latitude}, Longitude: {longitude}")
    latitude_user = latitude
    longitude_user = longitude
    return redirect('/test_page')


# Обработчик GET-запроса для отображения страницы с ближайшими спортивными залами
@app.route("/test_page")
def test_page():
    # Получаем данные о ближайших спортивных залах на основе координат пользователя
    data = get_gyms(latitude_user, longitude_user, db)

    places = []
    # Формируем список мест с их координатами для отображения на карте
    for item in data:
        place = {
            'name': item[0],
            'coords': [item[3], item[4]]
        }
        places.append(place)

    # Добавляем место пользователя на карту
    places.append({'name': 'Me', 'coords': [latitude_user, longitude_user]})

    # Отображаем шаблон страницы с картой и местами
    return render_template('index_map.html', latitude_user=latitude_user, longitude_user=longitude_user, places=places)
