from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from blog import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(40), index=True, default='User', nullable=False)
    last_seen = db.Column(db.DateTime)
    user_status = db.Column(db.String(140), nullable=True, default='Лучший пользователь проекта')
    comment = db.relationship('Comment', backref='author_comment', lazy=True)
    posts = db.relationship('Post', backref='author', lazy=True)

    # https://itsdangerous.palletsprojects.com/en/2.0.x/jws/
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @property
    def is_admin(self):
        return self.role == 'Admin'

    @property
    def is_moder(self):
        return self.role == 'Moder'

    @property
    def is_editor(self):
        return self.role == 'Editor'

    @property
    def is_user(self):
        return self.role == 'User'

    def __repr__(self):
        return self.username


class Post(db.Model):
    __tablename__ = "posts"
    __searchable__ = ['title', 'content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text(), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_post = db.Column(db.String(120), nullable=False, default='default.jpg')
    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    slug = db.Column(db.String(), unique=True, index=True)
    tags = db.relationship('Tag', backref='tag_post', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='comment_post', lazy=True, cascade="all, delete-orphan")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return self.title


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=False, nullable=False)
    body = db.Column(db.Text(), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    likes = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return self.username


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return self.name
