# Импорт необходимых модулей и классов
from app.models.user import User
from flask_admin.contrib.sqla import ModelView


# Представление таблицы с пользователями
class UserView(ModelView):
    column_list = User.__table__.columns.keys()
