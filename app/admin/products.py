from flask_admin.contrib.sqla import ModelView
from app.models.product import Product


class ProductView(ModelView):
    column_list = Product.__table__.columns.keys()