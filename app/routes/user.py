from app.forms.login import LoginForm
from app.forms.register import RegistrationForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user
from app.models.user import User
from app import db
from app import app, login_manager
from flask import render_template, redirect, url_for, session, flash


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))


@app.route("/log", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.mail.data
        password = form.password.data

        user = User.query.filter_by(mail=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            session['userID'] = user.id  # Save user ID in session
            name_last_name = f"{user.name} {user.last_name}"
            return redirect(url_for('index'))

        flash('Invalid email or password', 'error')

    return render_template('user/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(mail=form.mail.data).first()
        if existing_user:
            flash('User with this email already exists', 'error')
        else:
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

            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                session['userID'] = new_user.id
                return redirect(url_for('index'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Please try again.', 'error')

    return render_template('user/register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('userID', None)
    return redirect(url_for('index'))
