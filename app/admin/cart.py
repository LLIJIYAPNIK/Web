from flask_admin.contrib.sqla import ModelView
from app.models.cart import Cart


class CartView(ModelView):
    column_list = Cart.__table__.columns.keys()