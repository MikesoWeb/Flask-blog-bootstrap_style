import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

# Paths
# Констаты должны быть заглавными буквами
BASEDIR = os.path.abspath(os.path.dirname(__file__))
DB_DIRECTORY = 'DB/' 
DB_NAME = 'blog_sqlite.db'
USER_IMAGE_DIRECTORY = 'static/profile_pics/users'

def create_path_to_dir_db():
    """
    Создаем путь к папке с базой данных
    """   
    PATH_TO_DB_DIRECTORY = os.path.abspath(
    os.path.join(os.getcwd(), BASEDIR, DB_DIRECTORY))
    if not os.path.exists(PATH_TO_DB_DIRECTORY):
        os.mkdir(PATH_TO_DB_DIRECTORY)    


def last_seen_user(db, current_user):
    current_user.last_seen = datetime.now()
    db.session.commit()

def upload_folder():
    # Формирует путь к папке с изображениями
    # 'c:\\Users\\mike\\Desktop\\FlaskLikeCount\\blog\\static/profile_pics/users'
    return str(os.path.join(BASEDIR, USER_IMAGE_DIRECTORY))


load_dotenv(os.path.join(BASEDIR, '.env'))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'TEST_SECRET_KEY')
    WTF_CSRF_SECRET_KEY = "secrets.token_hex(16)"
    TEMPLATES_AUTO_RELOAD = False
    DEBUG = False
    TESTING = False


class ConfigDebug(Config):
    DEBUG = True
    TESTING = True
    TEMPLATES_AUTO_RELOAD = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        DB_DIRECTORY + DB_NAME


class ConfigProd(Config):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///prod.db'
    # SERVER_NAME = 'localhost:5667'

    # Безопасность
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    #  Настройки postgresql
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        os.environ.get('DB_ENGINE', default='postgresql'),
        os.environ.get('DB_USERNAME', default='postgres'),
        os.environ.get('DB_PASS', default='qwerty'),
        os.environ.get('DB_HOST', default='localhost'),
        os.environ.get('DB_PORT', default=5432),
        os.environ.get('DB_NAME', default='flask_new')
    )


# Bootstrap settings

BABEL_DEFAULT_LOCALE = 'ru'
BOOTSTRAP_BTN_STYLE = 'btn btn-outline-primary'
BOOTSTRAP_BTN_SIZE = 'sm'


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
