# Импорт необходимых модулей и классов
from flask_admin.contrib.sqla import ModelView
from app.models.gym import Gyms


# Представление фитнес-клубов
class GymsView(ModelView):
    column_list = Gyms.__table__.columns.keys()
