from flask_admin import AdminIndexView, expose


class DashboardView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('dashboard_index.html')
