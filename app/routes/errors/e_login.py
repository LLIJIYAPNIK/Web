# Импорт необходимых модулей и классов
from app import app
from flask import render_template


# Обработчик ошибки 401 (пользователь не авторизован)
@app.errorhandler(401)
def login_error(e):
    return render_template('errors/login_error.html'), 401
