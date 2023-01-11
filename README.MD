Блог на веб-фреймворке Flask языка программирования Python

Модели:
- User
- Post
- Comment
- Tag

Посмотреть на проект [Блог на Flask](https://flask-blog.my-py.ru/) в сети


Приложение имеет возможность работать с sqlite так и с postgresql базами данных
Для этого реализованы две конфигурации, которые принимают из файла .env ваши настройки

    использованы модули:

        flask
        flask-wtf
        flask-login
        flask-sqlalchemy
        flask-bcrypt
        flask-babel
        bootstrap-flask
        python-dotenv
        email-validator
        ...


В корне проекта создадим виртуальное окружение и активируем его

    python -m venv flaskvenv
    flaskvenv\Scripts\activate

А дальше нужно установить все зависимости проекта в это окружение
В папке requirements находятся зависимости проекта. 
    
    pip install -r requirements/dev.txt  для dev-разработки
    pip install -r requirements/prod.txt для продакшена (PostgreSQL)

В папке проекта создать файл .env и записать в него свои значения переменных окружения,
как указано в примере файла .env.template


Для запуска проекта используется файл

    run.py

#Внимание
База данных создается при запуске:

    Или на windows запускаем run    (run.bat)
    Или на linux запускаем run    (run.sh)


- Для запуска в Docker есть Dockerfile

**[_Михаил Терехов, 2022 год_](https://www.youtube.com/@PythonDevelopment)**
