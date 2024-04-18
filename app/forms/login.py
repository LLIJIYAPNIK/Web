# Импорт необходимых модулей и классов
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


# Форма для авторизации
class LoginForm(FlaskForm):
    mail = StringField('Эл. почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
