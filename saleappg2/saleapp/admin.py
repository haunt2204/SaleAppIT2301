from flask import redirect
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.theme import Bootstrap4Theme
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from saleapp import app, db
from saleapp.models import Category, Product


class MyCategoryView(ModelView):
    column_list = ['name','created_date','products']
    column_searchable_list = ['name']
    column_filters = ['name']

    column_labels = {
        "name": "Tên loại",
        "created_date": "Ngày tạo",
        "products": "Danh sách sản phẩm"
    }

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class MyProductView(ModelView):
    column_list = ['name', 'created_date', 'category']
    column_searchable_list = ['name']
    column_filters = ['name']

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self) -> str:
        return self.render('admin/index.html')

class MyAdminLogoutView(BaseView):
    @expose('/')
    def index(self) -> str:
        logout_user()
        return redirect('/admin')

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

admin = Admin(app=app, name="E-Commerce", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyAdminLogoutView("Đăng xuất"))