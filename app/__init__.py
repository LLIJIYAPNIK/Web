# Импорт необходимых модулей и классов
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_msearch import Search
from flask_session import Session
from .config import Config

# Создание экземпляра приложения Flask
app = Flask(__name__)
app.config.from_object(Config)

# Инициализация объекта для работы с базой данных
db = SQLAlchemy(app)

# Инициализация объекта для работы с сессиями
session = Session(app)

# Инициализация объекта для поиска
search = Search(db=db)
search.init_app(app)

# Инициализация объекта для управления аутентификацией пользователей
login_manager = LoginManager(app)

# Импорт модулей и маршрутов
from . import get_nearst_gym
from routes import main, editor, location, profile, user, about_us
from .routes.post import search
from .routes import article
from admin import admin
from routes.post import all_posts, delete, edit, get, post, publish, reaction, update
from routes.shop import main, product
from routes.shop.add import add_to_cart, add_to_cart_from_single, just_buy
from routes.shop.cart import cart, clear_cart, remove_from_cart, update_cart
from routes.errors import e_404, e_login
