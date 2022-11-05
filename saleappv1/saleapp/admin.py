from saleapp import db, app
from saleapp.models import Category, Product, UserRole
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask import redirect
from flask_login import logout_user, current_user

admin = Admin(app=app, name='Quản trị bán hàng', template_mode='bootstrap4')


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class ProductView(AuthenticatedModelView):
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    can_view_details = True
    column_exclude_list = ['image']
    can_export = True
    column_export_list = ['id', 'name', 'description', 'price']
    column_labels = {
        'name': 'Tên sản phẩm',
        'description': 'Mô tả',
        'price': 'Gía'
    }


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


admin.add_view(AuthenticatedModelView(Category, db.session, name='Danh mục'))
admin.add_view(ProductView(Product, db.session, name='Sản phẩm'))
admin.add_view(StatsView(name='Thống kê - báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))

