Запуск приложения:
        1. Создание БД с помощью миграции
        2. Запуск tortoise_init.py
        3. Запуск приложения


Описание создания миграций: https://ashfakmeethal.medium.com/tortoise-orm-migrations-with-aerich-5ebb7238bed5
        1. Должны быть установлены следующие пакеты:
            pip install fastapi
            pip install uvicorn[standard]
            pip install tortoise-orm[asyncpg]
            pip install aerich
        2. Создаётся #models.py     
        3. Файл конфигурации БД # database.py
        4. $ aerich init -t auth.database.TORTOISE_ORM
            Success create migrate location ./migrations
            Success generate config file aerich.ini
        5. $ aerich init-db
            Success create app migrate location migrations/contact
            Success generate schema for app "contact"
        6. Для создания миграции в файл model.py добавляем нужное поле (лучше со значением по умолчанию )
            и СОХРАНЯЕМ файл
            email = fields.CharField(max_length=100, default="fake_email")
        7. $ aerich migrate --name add_email
            Success migrate 1_20210508120617_add_email.sql
        8. $ aerich upgrade / $ aerich downgrade (Для удаления)
            Success upgrade 1_20210508120617_add_email.sql
