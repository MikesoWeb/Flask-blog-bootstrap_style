import os
import shutil

import sqlalchemy
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from blog import bcrypt, db
from blog.models import Post, User
from blog.settings import USER_IMAGE_DIRECTORY, last_seen_user, upload_folder
from blog.user.forms import (LoginForm, RegistrationForm, RequestResetForm,
                             ResetPasswordForm, UpdateAccountForm)
from blog.user.utils import random_avatar, save_picture, send_reset_email

users = Blueprint('users', __name__, template_folder='templates')


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    image_file=random_avatar(form.username.data))
        db.session.add(user)
        db.session.commit()

        flash('Ваш аккаунт был создан. Вы можете войти на блог', 'success')
        return redirect(url_for('users.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": {}'.format(getattr(form, field).label.text, error))

    return render_template('user/register.html', form=form, title='Регистрация', legend='Регистрация')


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Вы вошли как пользователь {current_user.username}', 'info')
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash('Войти не удалось. Пожалуйста, проверьте электронную почту или пароль', 'danger')
    return render_template('user/login.html', form=form, title='Логин', legend='Войти')


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(username=current_user.username).first()
    posts = Post.query.all()
    users = User.query.all()
    form = UpdateAccountForm()
    image_file = url_for('static',
                         filename=f'profile_pics' + '/users/' + current_user.username + '/account_img/' +
                                  current_user.image_file)
    return render_template('user/account.html', title='Аккаунт',
                           image_file=image_file, form=form, posts=posts, users=users, user=user)


@users.route('/user/<string:username>')
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=3)

    return render_template('user/user_posts.html', title='Общий блог', posts=posts, user=user)


@users.route('/user/action/<string:username>')
@login_required
def action_user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=3)

    return render_template('user/action_user.html', title='Общий блог', posts=posts, user=user)


@users.route('/user/edit/<string:username>', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=3)
    form = UpdateAccountForm()

    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.user_status.data = user.user_status
    # elif form.validate_on_submit():
    elif request.method == 'POST':
        
        
        # 'c:\\Users\\mike\\Desktop\\FlaskLikeCount\\blog\\static/profile_pics/users/mike'
        # 'c:\\Users\\mike\\Desktop\\FlaskLikeCount\\blog\\static/profile_pics/users/mikesoweb'
        path_one = os.path.join(upload_folder(),  user.username)
        path_two = os.path.join(upload_folder(), form.username.data)
               
        os.rename(path_one, path_two)
        
        user.email = form.email.data
        

        user.user_status = form.user_status.data

        if form.picture.data:
            try:
                user.image_file = save_picture(form.picture.data, user)
            
            except FileNotFoundError:
                ...
        else:
            form.picture.data = user.image_file

        db.session.commit()
        flash('Ваш аккаунт был обновлён!', 'success')
        return redirect(url_for('users.user_posts', username=user))
    image_file = url_for('static',
                         filename=f'profile_pics' + '/users/' + user.username + '/account_img/' +
                                  user.image_file)

    return render_template('user/edit_info.html', title='Обновление', image_file=image_file, form=form, posts=posts,
                           users=users, user=user)


@users.route('/user/settings/<string:username>')
@login_required
def settings_user(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=3)

    return render_template('user/settings_user.html', title='Общий блог', posts=posts, user=user)


@users.route('/user_delete/<string:username>', methods=['GET', 'POST'])
@login_required
def delete_user(username):
    try:
        user = User.query.filter_by(username=username).first_or_404()
        if user and not user.is_admin:
            db.session.delete(user)
            db.session.commit()
            full_path = os.path.join(os.getcwd(), USER_IMAGE_DIRECTORY, user.username)
            shutil.rmtree(full_path)

            flash(f'Пользователь {username} был удалён!', 'info')
            return redirect(url_for('users.account'))

    except sqlalchemy.exc.IntegrityError:
        flash(f'У пользователя {username} есть контент!', 'warning')
        return redirect(url_for('users.account'))
    except FileNotFoundError:
        return redirect(url_for('users.account'))

    else:
        flash('Администрация!', 'info')
        return redirect(url_for('users.account'))


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('На указанный емайл были отправлены инструкции по восстановлению пароля', 'info')
        return redirect(url_for('users.login'))
    return render_template('user/reset_request.html', form=form, title='Сброс пароля')


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.blog'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Не правильный или просроченный токен', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль был обновлён! Вы можете войти на блог', 'success')
        return redirect(url_for('users.login'))
    return render_template('user/reset_token.html', form=form, title='Новый пароль')


@users.route('/api/add_admin/<string:username>')
@login_required
def add_admin(username):
    user = User.query.filter_by(username=username).first()
    if not user.is_admin:
        user.role = 'Admin'
        user.user_status = 'Администратор проекта'
        db.session.commit()
        flash('Пользователь получил роль администратора', 'success')
        return redirect(url_for('users.account'))
    else:
        flash('Пользователь уже обладает правами администратора', 'success')
        return redirect(url_for('users.account'))


@users.route('/api/del_admin/<string:username>', methods=['GET', 'POST'])
@login_required
def delete_admin(username):
    del_admin = User.query.filter_by(username=username).first()
    if del_admin.is_admin:
        del_admin.role = 'User'
        del_admin.user_status = 'Обычный пользователь'
        db.session.commit()
        flash('Пользователь получил роль обычного пользователя', 'success')
        return redirect(url_for('users.account'))
    else:
        flash('Вы уже обычный пользователь', 'success')
        return redirect(url_for('users.account'))


@users.route('/logout')
def logout():
    last_seen_user(db, current_user)
    logout_user()
    return redirect(url_for('main.home'))
