from flask import abort, flash, url_for
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_login import current_user, login_required


class DashBoardView(AdminIndexView):
    @login_required
    @expose('/')
    def admin_panel(self):
        if not (current_user.is_admin or current_user.is_moder):
            flash('У вас нет доступа к административной части блога', 'danger')
            abort(403)
        from blog.models import User
        all_users = User.query.all()
        image_file = url_for('static',
                             filename=f'profile_pics' + '/users/' + current_user.username + '/account_img/' +
                                      current_user.image_file)
        return self.render('admin/index_admin.html', all_users=all_users, image_file=image_file)


class OnBlogView(BaseView):
    @expose('/')
    def on_blog(self):
        return self.render('main/index.html')


admin = Admin(name='Admin Board', template_mode='bootstrap3',
              index_view=DashBoardView(), endpoint='admin')
