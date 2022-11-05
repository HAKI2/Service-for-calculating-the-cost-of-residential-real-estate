from flask import redirect, url_for
from flask_admin import AdminIndexView, Admin
from flask_admin.contrib.sqla import ModelView
from service.database.models import user
from flask_login import current_user


class MyUserAdmin(ModelView):
    def __init__(self, session, name, excluded=None):
        if excluded:
            self.column_exclude_list = excluded
            self.form_excluded_columns = excluded

        super(MyUserAdmin, self).__init__(user, session, name=name)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('admin_base.login'))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def _handle_view(self, name):
        if not self.is_accessible():
            return redirect(url_for('admin_base.login'))


def init_app(app, db, name="Admin", url_prefix="/admin", **kwargs):
    vkwargs = {"name": name, "endpoint": "admin_panel", "url": url_prefix, 'template': 'admin_panel.html'}

    akwargs = {
        "template_mode": "bootstrap4",
        "static_url_path": f"/templates/{url_prefix}",
        "index_view": MyAdminIndexView(**vkwargs),
    }

    admin = Admin(app, **akwargs)
    admin.add_view(MyUserAdmin(db.session, 'Пользователи'))
