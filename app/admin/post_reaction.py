from flask_admin.contrib.sqla import ModelView
from app.models.post_reaction import PostReactions


class PostReactionsView(ModelView):
    column_list = PostReactions.__table__.columns.keys()
