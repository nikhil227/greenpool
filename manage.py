from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

import config
from app import app, db

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('run', Server(host='localhost', port=config.CONFIG['port']))
manager.add_command('db', MigrateCommand)


if __name__ ==  '__main__':
    manager.run()
