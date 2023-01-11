from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_msearch import Search
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData

from blog.settings import ConfigDebug, ConfigProd, create_path_to_dir_db
from blog.views.admin_view import OnBlogView, admin

metadata = MetaData(
    naming_convention={
        'pk': 'pk_%(table_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'ix': 'ix_%(table_name)s_%(column_0_name)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
    }
)

db = SQLAlchemy(metadata=metadata, session_options={"autoflush": False})
bcrypt = Bcrypt()
migrate = Migrate()
bootstrap = Bootstrap5()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Авторизуйтесь, чтобы попасть на эту страницу!'
mail = Mail()
search = Search()
babel = Babel()


def register_extensions(app):
    # Регистрируем все расширения приложения
    db.init_app(app)
    admin.init_app(app)
    bcrypt.init_app(app)
    babel.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    mail.init_app(app)
    search.init_app(app)
    bootstrap.init_app(app)
    csrf.init_app(app)

def register_admin(admin):
    from blog.models import Comment, Post, Tag, User
    from blog.views.post_view import PostView
    from blog.views.user_view import UserView

    admin.add_view(OnBlogView(name='На блог'))
    admin.add_view(UserView(User, db.session, name='Пользователь'))
    admin.add_view(PostView(Post, db.session, name='Статьи'))
    admin.add_view(ModelView(Comment, db.session, name='Комментарии'))
    admin.add_view(ModelView(Tag, db.session, name='Теги'))


def register_blueprints(app):
    from blog.errors.handlers import errors
    from blog.main.routes import main
    from blog.post.routes import posts
    from blog.user.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

def configure_database(app):
    create_path_to_dir_db()
    
    @app.before_first_request
    def initialize_database():        
        db.create_all()
        
    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
        

def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigDebug)
    register_extensions(app)
    configure_database(app)
    register_admin(admin)
    register_blueprints(app)

    return app
