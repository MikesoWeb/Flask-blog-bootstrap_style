import os

import PIL
import sqlalchemy
from flask import (Blueprint, abort, current_app, flash, redirect,
                   render_template, request, url_for)
from flask_login import current_user, login_required
from slugify import slugify

from blog import db
from blog.models import Comment, Post, Tag
from blog.post.forms import CommentUpdateForm, PostForm, PostUpdateForm
from blog.post.utils import form_path_user_image, save_picture_post_author
from blog.user.forms import AddCommentForm

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    try:
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, category=form.category.data,
                        image_post=form.picture.data, author=current_user)
            db.session.add(post)
            post.slug = slugify(post.title)
            post.image_post = save_picture_post_author(form.picture.data, post)
            db.session.flush()

            name = form.tag_form.data.split('/')
            for i in name:
                tag_post = Tag(name=i)  # создаю тег
                tag_post.post_id = post.id
                db.session.add(tag_post)
            db.session.commit()
            flash('Пост был опубликован!', 'success')

            return redirect(url_for('main.blog'))
        else:
            if request.method == 'POST':
                flash('Формат изображения должен быть "jpg", "png"', 'success')

    except PIL.UnidentifiedImageError:
        flash('Выберите изображение для статьи', 'danger')
    except sqlalchemy.exc.IntegrityError:
        flash('Такой заголовок уже существует', 'danger')
        db.session.rollback()

    # form_path_user_image()
    image_file = url_for('static',
                         filename=form_path_user_image(current_user.username) + current_user.image_file)
    return render_template('post/create_post.html', title='Новая статья',
                           form=form, legend='Новая статья', image_file=image_file)


# http://wtforms.simplecodes.com/docs/0.6.1/fields.html#custom-fields
# https://stackoverflow.com/questions/62065605/how-to-add-a-list-of-tags-to-a-flask-wtforms-jinja2-form
# https://gist.github.com/M0r13n/71655c53b2fbf41dc1db8412978bcbf9

def set_view_post(post):
    # Инкрементит количество просмотров поста
    # Нужно сделать защиту от накруток!
    post.views += 1
    db.session.commit()


def add_tag(form_post, post):
    name = form_post.tag_form.data
    if name:
        name = name.split('/')
        for i in name:
            tag_post = Tag(name=i)  # создаю тег
            tag_post.post_id = post.id
            db.session.add(tag_post)
        db.session.commit()
        flash('Тег к посту был добавлен', "success")
        return redirect(url_for('posts.post', slug=post.slug))


@posts.route('/post/<string:slug>', methods=['GET', 'POST'])
@login_required
def post(slug):
    post = Post.query.filter_by(slug=slug).first()
    comment = Comment.query.filter_by(post_id=post.id).order_by(
        db.desc(Comment.date_posted)).all()
    # print(comment)

    set_view_post(post)

    form_post = PostForm()
    form_comment = AddCommentForm()
    if request.method == 'POST':

        # Добавляем тег или список тегов к посту
        add_tag(form_post, post)

    if request.method == 'POST' and form_comment.validate_on_submit():
        username = current_user.username
        comment = Comment(username=username, body=form_comment.body.data,
                          post_id=post.id, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий к посту был добавлен', "success")
        return redirect(url_for('posts.post', slug=post.slug))
    form_post.tag_form.data = ''
    # form_path_user_image()
    image_file = url_for('static',
                         #  filename=f'profile_pics/' + 'users/' + post.author.username + '/post_images/' + post.image_post)
                         filename=form_path_user_image(post.author.username) + post.image_post)
    print(image_file)
    return render_template('post/post.html', title=post.title, post=post, image_file=image_file,
                           form_add_comment=form_comment, comment=comment, form_add_tag=form_post)


@posts.route('/post/search')
@login_required
def search():
    try:
        keyword = request.args.get('q')
        search_posts = Post.query.msearch(
            keyword, fields=['title', 'content'], limit=6)
        if keyword and search_posts:
            return render_template('post/search.html', search_posts=search_posts, title='Поиск')

        else:
            flash('Введите что-то в поле поиска', 'danger')
            return redirect(url_for('main.blog'))

    except AttributeError as e:
        raise e


@posts.route('/post/<string:slug>/update', methods=['GET', 'POST'])
@login_required
def update_post(slug):
    post = Post.query.filter_by(slug=slug).first()

    # чтобы не смогли обновить чужую статью
    if post.author != current_user:
        flash('Нет доступа к обновлению статьи!', 'danger')
        return redirect(url_for('posts.post', slug=post.slug))
    form = PostUpdateForm()
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.category.data = post.category

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.slug = slugify(post.title)
        db.session.commit()

        if form.picture.data:
            post.image_post = save_picture_post_author(form.picture.data, post)
        db.session.commit()
        flash('Данный пост был обновлён', 'success')

        return redirect(url_for('main.home'))
    else:
        if request.method == 'POST':
            flash('Формат изображения должен быть "jpg", "png"', 'success')

    # test_user_image_file()
    image_file = url_for('static',
                         filename=form_path_user_image(current_user.username) + post.image_post)

    return render_template('post/update_post.html', title='Обновление ' + post.title,
                           form=form, legend='Обновить статью', image_file=image_file, post=post)


@posts.route('/post/comment/<int:comment_id>/update/', methods=['GET', 'POST'])
@login_required
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    form = CommentUpdateForm()
    if current_user.is_admin or comment.username == current_user.username:

        if request.method == 'GET':
            form.body.data = comment.body

        if request.method == 'POST' and form.validate_on_submit():
            comment.body = form.body.data
            db.session.commit()
            return redirect(url_for('posts.post', slug=comment.comment_post.slug))
    else:
        abort(403)
    return render_template('post/update_comment.html', form_comment_update=form, title="Обновление комментария")


@posts.route('/posts/<string:category_str>/', methods=['GET', 'POST'])
@login_required
def category(category_str):
    current_category = Post.query.filter_by(category=category_str).first()
    posts_category = Post.query.filter_by(category=category_str).all()
    return render_template('post/all_posts_category.html', post_category=posts_category,
                           current_category=current_category, title='Рубрика ' + category_str)


@posts.route('/tags/<string:tag_str>', methods=['GET', 'POST'])
@login_required
def tag(tag_str):
    current_tag = Tag.query.filter_by(name=tag_str).first_or_404()
    name_tags = Tag.query.filter(Tag.name == current_tag.name).all()
    return render_template('post/all_post_tag.html', name_tags=name_tags,
                           current_tag=current_tag, title='Статьи тега ' + current_tag.name)


@posts.route('/post/<string:slug>/add_like_post', methods=['GET', 'PUT'])
@login_required
def add_like_post(slug):
    post = Post.query.filter_by(slug=slug).first()
    post.likes += 1
    db.session.commit()
    flash('Лайк к посту добавлен', 'success')
    return redirect(url_for('posts.post', slug=post.slug))


@posts.route('/post/<string:slug>/add_like_comment', methods=['GET', 'PUT'])
@login_required
def add_like_comment(slug):
    post = Post.query.filter_by(slug=slug).first()
    comment = Comment.query.filter_by(post_id=post.id).order_by(
        db.desc(Comment.date_posted)).first()
    comment.likes += 1
    db.session.commit()
    flash('Лайк к комментарию добавлен', 'success')
    return redirect(url_for('posts.post', slug=post.slug))


@posts.route('/post/<string:slug>/delete', methods=['DELETE', 'GET'])
@login_required
def delete_post(slug):
    post = Post.query.filter_by(slug=slug).first()
    if post.author != current_user:
        abort(403)
    try:
        db.session.delete(post)
        # form_path_user_image()
        # os.unlink(url_for('static',
        #                  filename=form_path_user_image(current_user.username) + post.image_post))
        os.unlink(
            os.path.join(current_app.root_path,
                         f'static/profile_pics/users/{current_user.username}/post_images/{post.image_post}'))

    except:
        db.session.delete(post)
        # print('Не могу удалить пост!')

    db.session.commit()
    flash('Данный пост был удален', 'success')
    return redirect(url_for('users.account'))


# post = Post.query.filter_by(slug=single_comment.comment_post.slug).first()
# Post(1, New post, 2021-12-15 12:34:24.444376, bf3f68498d4e8ef464e1ee806d933f1b.jpg, 1)

@posts.route('/post/comment/<int:comment_id>/delete')
@login_required
def delete_comment(comment_id):
    single_comment = Comment.query.get_or_404(comment_id)
    return_to_post = single_comment.comment_post.slug
    print('COMMENT DELETE', single_comment)

    if current_user.is_admin or single_comment.username == current_user.username:
        db.session.delete(single_comment)
        db.session.commit()
        flash('Комментарий был удалён', 'success')
    else:
        abort(403)
    return redirect(url_for('posts.post', slug=return_to_post))


@posts.route('/post/tag/<int:tag_id>/delete')
@login_required
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if tag.tag_post.author != current_user:
        abort(403)
    db.session.delete(tag)
    db.session.commit()
    flash('Тег удален', 'success')
    return redirect(url_for('posts.post', slug=tag.tag_post.slug))
