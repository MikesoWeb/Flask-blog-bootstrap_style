from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (BooleanField, FileField, PasswordField, SelectField,
                     StringField, SubmitField)
from wtforms.validators import (DataRequired, Email, EqualTo, InputRequired,
                                Length, ValidationError)

from blog.models import User
from blog.settings import AVAILABLE_USER_TYPES


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=120)],
                           render_kw={'class': 'form-control'})
    email = StringField('Емайл', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    # role = SelectField('Роли', choices=AVAILABLE_USER_TYPES)
    submit = SubmitField('Войти')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('Это имя уже занято. Пожалуйста, выберите другое', 'danger')
            raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('Этот емайл уже занят. Пожалуйста, введите другой', 'danger')
            raise ValidationError('That email is taken. Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Емайл', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class AddCommentForm(FlaskForm):
    body = StringField("Ваш комментарий", validators=[InputRequired()])
    submit = SubmitField("Комментировать")


class UpdateAccountForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Емайл', validators=[DataRequired(), Email()])
    picture = FileField('Изображение (png, jpj)', validators=[FileAllowed(['jpg', 'png']), ])
    user_status = StringField('Статус', validators=[DataRequired(), Length(min=4, max=40)])
    submit = SubmitField('Обновить')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                flash('Это имя уже занято. Пожалуйста, выберите другое', 'danger')
                raise ValidationError('That username is taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                flash('Этот емайл уже занят. Пожалуйста, введите другой', 'danger')
                raise ValidationError('That email is taken. Please choose a different one')


class RequestResetForm(FlaskForm):
    email = StringField('Емайл', validators=[DataRequired(), Email()])
    submit = SubmitField('Сбросить пароль')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            flash('Нет аккаунта с такой электронной почтой', 'danger')
            raise ValidationError('Нет аккаунта с такой электронной почтой')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Сбросить пароль')
