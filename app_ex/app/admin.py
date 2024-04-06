from flask_admin import Admin, BaseView, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from models import User, Posts, db, PostReactions, Gyms
from app_ex.app import admin


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


admin.index_view = DashboardView()
admin.add_view(UserView(User, db.session))
admin.add_view(PostsView(Posts, db.session))
admin.add_view(PostReactionsView(PostReactions, db.session))
admin.add_view(GymsView(Gyms, db.session))
