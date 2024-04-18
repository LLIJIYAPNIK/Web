# Импорт необходимых модулей и классов
from flask import render_template
from app import app


# Маршрут для статьи о самостоятельных тренировках
@app.route('/independent_training')
def independent_training():
    return render_template("articles/independent_training.html")


# Маршрут для статьи о групповых тренировках
@app.route("/group_classes")
def group_classes():
    return render_template("articles/group_classes.html")


# Маршрут для статьи о персональных тренировках
@app.route('/personal_training')
def personal_training():
    return render_template("articles/personal_training.html")
