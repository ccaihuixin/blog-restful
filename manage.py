import os

from flask_script import Manager

from app import create_app  # 不指定模块名默认是__init__.py文件
from flask_migrate import Migrate, MigrateCommand
from app.extensions import db

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
# 添加命令行启动控制
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manager.run()
