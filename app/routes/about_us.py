# Импорт необходимых модулей и классов
from flask import render_template
from app import app


# Маршрут для отображения страницы "О нас"
@app.route('/about-us')
def about_us():
    return render_template("about-us.html")
