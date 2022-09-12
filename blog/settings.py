import os
from datetime import timedelta

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(basedir, 'blog/.env'))

# SECRET_KEY = os.urandom(36)
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
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


