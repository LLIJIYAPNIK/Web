# Импорт необходимых модулей и классов
from flask_admin.contrib.sqla import ModelView
from app.models.post import Posts


# Представление статей
class PostsView(ModelView):
    column_list = Posts.__table__.columns.keys()
