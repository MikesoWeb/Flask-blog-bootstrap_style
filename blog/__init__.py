from flask import Flask, url_for, abort, flash
from flask_admin import Admin, expose, AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_msearch import Search
from flask_babelex import Babel
from flask_bootstrap import Bootstrap5
from sqlalchemy import MetaData

metadata = MetaData(
  naming_convention={
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    }
)

db = SQLAlchemy(metadata=metadata)

bcrypt = Bcrypt()
migrate = Migrate()
bootstrap = Bootstrap5()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Авторизуйтесь, чтобы попасть на эту страницу!'

mail = Mail()
search = Search()
babel = Babel()


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


class OnBlog(BaseView):
    @expose('/')
    def on_blog(self):
        return self.render('main/index.html')


admin = Admin(name='Admin Board', template_mode='bootstrap3', index_view=DashBoardView(), endpoint='admin')


def create_app():
    app = Flask(__name__)
    admin.init_app(app)
    app.config.from_pyfile('settings.py')
    db.init_app(app)
    bcrypt.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    mail.init_app(app)
    search.init_app(app)
    bootstrap.init_app(app)

    from blog.models import User, Post, Comment, Tag
    from blog.views.user_view import UserView
    from blog.views.post_view import PostView

    admin.add_view(OnBlog(name='На блог'))
    admin.add_view(UserView(User, db.session, name='Пользователь'))
    admin.add_view(PostView(Post, db.session, name='Статьи'))
    admin.add_view(ModelView(Comment, db.session, name='Комментарии'))
    admin.add_view(ModelView(Tag, db.session, name='Теги'))

    from blog.main.routes import main
    from blog.user.routes import users
    from blog.post.routes import posts
    from blog.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app
