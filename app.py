from flask import render_template, request, redirect, url_for, session, flash
from get_nearst_gym import get_gyms
from forms import LoginForm, RegisterForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mflkdmklbmkldmaklbsmdrfkoigbhjmnoikmd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://Sasha:Sasha@localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

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
    data = get_gyms(latitude_user, longitude_user, db)

    places = []
    for item in data:
        place = {
            'name': item[0],
            'coords': [item[3], item[4]]
        }
        places.append(place)
    places.append({'name': 'Me', 'coords': [latitude_user, longitude_user]})

    return render_template('index_map.html', latitude_user=latitude_user, longitude_user=longitude_user, places=places)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


@app.route("/log", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.mail.data
        password = form.password.data

        user = db.session.query(User).filter_by(mail=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            name_last_name = f"{user.name} {user.last_name}"
            return redirect(url_for('index'))

        flash('Invalid username or password', 'error')

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

        if new_user.id:
            login_user(new_user)
            return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/index_login')
def index_login():
    data = request.args.get('data')
    user = str(data)
    return render_template('index_login.html', user=user)


@app.route('/editor')
@login_required
def editor():
    return render_template('editor.html')



if __name__ == "__main__":
    app.run(debug=True)
