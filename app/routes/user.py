# Импорт необходимых модулей и классов
from app.forms.login import LoginForm
from app.forms.register import RegistrationForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user
from app.models.user import User
from app import db
from app import app, login_manager
from flask import render_template, redirect, url_for, session, flash


# Загрузка пользователя из базы данных по его идентификатору
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Маршрут для входа пользователя в систему
@app.route("/log", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # Если форма отправлена и прошла валидацию
    if form.validate_on_submit():
        # Поиск пользователя по адресу электронной почты
        user = User.query.filter_by(mail=form.mail.data).first()
        # Проверка наличия пользователя и соответствия пароля
        if user and check_password_hash(user.password, form.password.data):
            # Вход пользователя в систему
            login_user(user)
            # Сохранение идентификатора пользователя в сессии
            session['userID'] = user.id
            # Перенаправление на главную страницу после успешного входа
            return redirect(url_for('index'))
        # Вывод сообщения об ошибке при неверном адресе электронной почты или пароле
        flash('Invalid email or password', 'error')
    # Рендеринг шаблона для страницы входа
    return render_template('user/login.html', form=form)


# Маршрут для регистрации нового пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # Если форма отправлена и прошла валидацию
    if form.validate_on_submit():
        # Проверка наличия пользователя с таким же адресом электронной почты
        existing_user = User.query.filter_by(mail=form.mail.data).first()
        if existing_user:
            # Вывод сообщения об ошибке, если пользователь с таким адресом электронной почты уже существует
            flash('Пользователь с таким адресом электронной почты уже существует', 'error')
        else:
            # Генерация хеша и соли пароля
            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )

            # Создание нового пользователя
            new_user = User(
                mail=form.mail.data,
                name=form.name.data,
                last_name=form.last_name.data,
                password=hash_and_salted_password
            )

            try:
                # Добавление нового пользователя в сессию базы данных
                db.session.add(new_user)
                # Подтверждение изменений в базе данных
                db.session.commit()
                # Вход пользователя в систему
                login_user(new_user)
                # Сохранение идентификатора пользователя в сессии
                session['userID'] = new_user.id
                # Перенаправление на главную страницу после успешной регистрации
                return redirect(url_for('index'))
            except Exception as e:
                # Откат изменений в случае ошибки
                db.session.rollback()
                # Вывод сообщения об ошибке при регистрации
                flash('Произошла ошибка при регистрации. Пожалуйста, попробуйте еще раз.', 'error')

    # Рендеринг шаблона для страницы регистрации
    return render_template('user/register.html', form=form)

    # Маршрут для выхода пользователя из системы


@app.route('/logout')
@login_required
def logout():
    # Выход пользователя из системы
    logout_user()
    # Удаление идентификатора пользователя из сессии
    session.pop('userID', None)
    # Перенаправление на главную страницу после выхода
    return redirect(url_for('index'))
