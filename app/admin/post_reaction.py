# Импорт необходимых модулей и классов
from flask_admin.contrib.sqla import ModelView
from app.models.post_reaction import PostReactions


# Представление реакций
class PostReactionsView(ModelView):
    column_list = PostReactions.__table__.columns.keys()
