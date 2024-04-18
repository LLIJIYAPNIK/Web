# Импорт необходимых модулей и классов
from flask_admin.contrib.sqla import ModelView
from app.models.cart import Cart


# Представление корзины
class CartView(ModelView):
    column_list = Cart.__table__.columns.keys()