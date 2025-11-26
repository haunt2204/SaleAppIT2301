from flask import redirect
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from saleapp import app, db
from saleapp.models import Category, Product, User, UserRole
from flask_admin import BaseView
from flask_login import logout_user, current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class MyAuthenticatedView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated and current_user.role==UserRole.ADMIN


class MyCategoryView(MyAuthenticatedView):
    column_list = ["id", "name", "products"]
    column_searchable_list = ["name"]
    column_filters = ["name"]


class MyProductView(MyAuthenticatedView):
    column_list = ['name', 'price', 'image', 'category', 'description']
    column_searchable_list = ["name"]
    column_filters = ["category", "name"]
    column_labels = {
        "name": "Tên sản phẩm",
        "price": "Giá"
    }
    can_export = True
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }

class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render('admin/index.html')

class MyLogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")

    def is_accessible(self) -> bool:
        return current_user.is_authenticated

admin = Admin(app=app, name="E-COMMERCE", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyLogoutView("Đăng xuất"))

