from flask_admin import Admin, BaseView, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from models import User, Posts, db, PostReactions, Gyms


class DashboardView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('dashboard_index.html')


class UserView(ModelView):
    column_list = User.__table__.columns.keys()


class PostsView(ModelView):
    column_list = Posts.__table__.columns.keys()


class GymsView(ModelView):
    column_list = Gyms.__table__.columns.keys()


class PostReactionsView(ModelView):
    column_list = PostReactions.__table__.columns.keys()
