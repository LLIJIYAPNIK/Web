from flask_admin.contrib.sqla import ModelView
from app.models.post import Posts


class PostsView(ModelView):
    column_list = Posts.__table__.columns.keys()
