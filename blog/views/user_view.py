import os

from flask import Markup, url_for
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from wtforms import validators

from blog import bcrypt
from blog.settings import AVAILABLE_USER_TYPES

file_path = os.path.abspath(os.path.dirname(__name__))


# Функция, которая будет генерировать имя файла из модели и загруженного файлового объекта.
def name_gen_image(model, file_data):
    hash_name = f'{model}/{model.username}'
    return hash_name


class UserView(ModelView):
    column_display_pk = True
    column_labels = {
        'id': 'ID',
        'username': 'Имя пользователя',
        'last_seen': 'Последний вход',
        'image_file': 'Аватар',
        'posts': 'Посты',
        'email': 'Емайл',
        'password': 'Пароль',
        'role': 'Роль',
        'file': 'Выберите изображение',
        'user_status': 'Статус пользователя',
    }

    # Список отображаемых колонок
    column_list = ['id', 'role', 'username', 'email', 'password', 'last_seen', 'image_file']

    column_default_sort = ('username', True)
    column_sortable_list = ('id', 'role', 'username', 'email')

    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    export_max_rows = 500
    export_types = ['csv']

    form_args = {
        'username': dict(validators=[validators.DataRequired()]),
        'email': dict(validators=[validators.Email()]),
        'password': dict(validators=[validators.DataRequired()]),
    }

    form_choices = {
        'role': AVAILABLE_USER_TYPES,
    }

    # Словарь, где ключ — это имя столбца, а значение — описание столбца представления списка или поля формы добавления/редактирования.
    column_descriptions = dict(
        username='Имя пользователя'
    )

    # исключенные колонки
    column_exclude_list = ['password']

    column_searchable_list = ['email', 'username']
    column_filters = ['email', 'username']
    column_editable_list = ['role', 'username', 'email']

    # create_modal = True
    # edit_modal = True

    # Исключить колонку из создания, редактирования
    form_excluded_columns = ['']

    def _list_thumbnail(view, context, model, name):
        if not model.image_file:
            return ''

        url = url_for('static',
                      filename=os.path.join(f'profile_pics/users/{model.username}/account_img/{model.image_file}'))
        if model.image_file.split('.')[-1] in ['jpg', 'jpeg', 'png', 'svg', 'gif']:
            return Markup(f'<img src={url} width="100">')

    # передаю функцию _list_thumbnail в поле image_file
    column_formatters = {
        'image_file': _list_thumbnail
    }

    form_extra_fields = {
        # ImageUploadField Выполняет проверку изображений, создание эскизов, обновление и удаление изображений.
        "image_file": form.ImageUploadField('',
                                            # Абсолютный путь к каталогу, в котором будут храниться файлы
                                            base_path=
                                            os.path.join(file_path, 'blog/static/storage/user_img/'),
                                            # Относительный путь из каталога. Будет добавляться к имени загружаемого файла.
                                            url_relative_path='storage/user_img/',
                                            namegen=name_gen_image,
                                            # Список разрешенных расширений. Если не указано, то будут разрешены форматы gif, jpg, jpeg, png и tiff.
                                            allowed_extensions=['jpg'],
                                            max_size=(1200, 780, True),
                                            thumbnail_size=(100, 100, True),

                                            )}

    def create_form(self, obj=None):
        return super(UserView, self).create_form(obj)

    def edit_form(self, obj=None):
        return super(UserView, self).edit_form(obj)

    def on_model_change(self, view, model, is_created):
        if is_created:
            model.password = bcrypt.generate_password_hash(model.password)
        else:
            view.password.data = model.password
            view.role.data = model.role
