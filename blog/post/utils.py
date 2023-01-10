import os
import secrets

from flask import url_for
from PIL import Image
from flask import current_app
from flask_login import current_user
from blog.settings import users_image_dir


def form_path_user_image(username: str) -> str:
    # передаем в username имя пользователя для формирования 
    # маршрута к изображениям данного пользователя
    return f'/profile_pics/users/{username}/post_images/'


def path_to_post_user_img(username):
    """
    Возвращает путь к папке с изображениями постов пользователя
    """
  
    return os.path.join(current_app.root_path, users_image_dir, username, 'post_images')

def save_picture_post_author(form_picture, post):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    full_path = path_to_post_user_img(current_user.username)
    try:
        os.remove(
            os.path.join(current_app.root_path, 
                         f'static/profile_pics/users/{current_user.username}/post_images/{post.image_post}'))
                         
    except:
        print('Изображение не найдено, возможно оно было удалено!')
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    picture_path = os.path.join(full_path, picture_fn)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn