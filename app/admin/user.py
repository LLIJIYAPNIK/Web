from app.models.user import User
from flask_admin.contrib.sqla import ModelView


class UserView(ModelView):
    column_list = User.__table__.columns.keys()
