import os
from datetime import timedelta

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(basedir, 'blog/.env'))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.urandom(32)
    TEMPLATES_AUTO_RELOAD = False
    DEBUG = False
    TESTING = False
    


class ConfigDebug(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True   
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


class ConfigProd(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'
    SERVER_NAME = 'localhost:5667'


BABEL_DEFAULT_LOCALE = 'ru'
BOOTSTRAP_BTN_STYLE = 'btn btn-outline-primary'
BOOTSTRAP_BTN_SIZE = 'sm'
UPLOAD_FOLDER = os.path.join(basedir, 'blog', 'static', 'profile_pics', 'users')

REMEMBER_COOKIE_DURATION = timedelta(seconds=60)

AVAILABLE_USER_TYPES = [
    ('Admin', 'Администратор'),
    ('Moder', 'Модератор'),
    ('Editor', 'Редактор'),
    ('User', 'Пользователь'),
]

AVAILABLE_CATEGORY_POSTS = [
    ('html', 'HTML'),
    ('css', 'CSS'),
    ('python', 'Python'),
    ('js', 'JS'),
]

MAIL_USERNAME = os.environ.get('EMAIL_USER')
MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True


