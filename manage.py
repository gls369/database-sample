from flask_script import Manager, Server, Shell
from flask_migrate import MigrateCommand, Migrate
from app import app,db
from model import *
# 設定你的 app
manager = Manager(app)

manager.add_command('db',MigrateCommand)
# 設定 python manage.py runserver 為啟動 server 指令
manager.add_command('runserver', Server(host = 'localhost',port = 5000))

if __name__ == '__main__':
    manager.run()