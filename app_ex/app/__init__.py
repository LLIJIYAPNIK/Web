from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_msearch import Search
from flask_session import Session
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

session = Session(app)

search = Search()

login_manager = LoginManager(app)

admin = Admin(app, template_mode='bootstrap3')

from . import forms, get_nearst_gym, models, routes