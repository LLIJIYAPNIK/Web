from flask_admin import Admin
from app.models.user import User
from app.models.post import Posts
from app.models.post_reaction import PostReactions
from app.models.gym import Gyms
from app.models.product import Product
from app.models.cart import Cart
from app import db, app
from app.admin.dashboard import DashboardView
from app.admin.gym import GymsView
from app.admin.post import PostsView
from app.admin.post_reaction import PostReactionsView
from app.admin.user import UserView
from app.admin.cart import CartView
from app.admin.products import ProductView

admin = Admin(app, template_mode='bootstrap3', index_view = DashboardView())
admin.add_view(UserView(User, db.session))
admin.add_view(PostsView(Posts, db.session))
admin.add_view(PostReactionsView(PostReactions, db.session))
admin.add_view(GymsView(Gyms, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(CartView(Cart, db.session))
