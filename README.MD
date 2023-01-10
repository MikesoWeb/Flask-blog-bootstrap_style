Flask blog


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
В файле requirements.txt находятся зависимости проекта. 
    
    pip install -r requirements.txt

В папке проекта создать файл .env и записать в него свои значения переменных окружения,
как указано в примере файла .env.template



Для запуска проекта используется файл

    run.py

!Внимание!  База данных при запуске run, как указано ниже должна быть уже создана
    Или на windows запускаем run    (run.bat)
    Или на linux запускаем run    (run.sh)

При запуске python run.py база будет создана, так как передается весь контекст приложения!


**_Михаил Терехов, 2022 год_**
