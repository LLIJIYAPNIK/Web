from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_msearch import Search
from flask_session import Session
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

session = Session(app)

search = Search(db=db)
search.init_app(app)

login_manager = LoginManager(app)

from . import get_nearst_gym
from routes import main, article, editor, location, profile, search, user
from admin import admin
from routes.post import all, delete, edit, get, post, publish, reaction, update
