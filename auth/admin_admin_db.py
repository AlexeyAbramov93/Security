from tortoise import Tortoise
from models import User
from passlib.hash import bcrypt
from tortoise import run_async


async def init():
    # Если БД создана генерируется исключение, если нет - то создаётся БД
    try:
        await Tortoise.init(db_url='sqlite://sql_app.db', modules={'models': ['__main__']})
        #await Tortoise.generate_schemas(safe=False) # safe=False генерирует исключ если БД уже создана
        await User.create(username='admin', password_hash=bcrypt.hash('admin'), disabled=False)
        print('Create admin admin in DB successfully')
    except:
        print("Failed to create admin admin in DB")

if __name__ == '__main__':
    run_async(init()) # run_async по выполнению всех операций init() завершает автоматически соединение с БД
