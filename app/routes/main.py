# Импорт необходимых модулей и классов
from flask import render_template
from app import app


# Маршрут для главной старницы сайта
@app.route("/")
def index():
    return render_template("index.html")


# То же самое, лол =)
@app.route("/home")
def home_page():
    return render_template('index.html')
