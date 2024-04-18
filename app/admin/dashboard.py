# Импорт необходимых модулей и классов
from flask_admin import AdminIndexView, expose


# Главная админки
class DashboardView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('dashboard_index.html')
