from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from get_nearst_gym import get_gyms
from forms import LoginForm, RegisterForm
from models import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask import flash
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from models import User, Gyms

app = Flask(__name__)
app.config["SECRET_KEY"] = '0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Sasha:Sasha@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
latitude_user = 0
longitude_user = 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home_page():
    return render_template('index.html')


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


@app.route("/test_page")
def test_page():
    data = get_gyms(latitude_user, longitude_user)

    places = []
    for item in data:
        place = {
            'name': item[0],
            'coords': [item[3], item[4]]
        }
        places.append(place)
    places.append({'name': 'Me', 'coords': [latitude_user, longitude_user]})

    return render_template('index_map.html', latitude_user=latitude_user, longitude_user=longitude_user, places=places)


@app.route("/log", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.mail.data
        password = form.password.data

        user = db.session.query(User).filter_by(mail=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('home_page'))

        return 'Invalid username or password'

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            mail=form.mail.data,
            name=form.name.data,
            last_name=form.last_name.data,
            password=hash_and_salted_password
        )

        db.session.add(new_user)
        db.session.commit()

        if new_user.id:  # Проверяем наличие id у нового пользователя
            session['username'] = new_user.mail
            return redirect(url_for('home_page'))

    return render_template('register.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
