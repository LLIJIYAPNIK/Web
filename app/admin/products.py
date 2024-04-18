# Импорт необходимых модулей и классов
from flask_admin.contrib.sqla import ModelView
from app.models.product import Product


# Представление предоставляемых товаров
class ProductView(ModelView):
    column_list = Product.__table__.columns.keys()