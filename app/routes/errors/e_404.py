# Импорт необходимых модулей и классов
from app import app
from flask import render_template


# Обработчик ошибки 404 (страница не найдена)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404
