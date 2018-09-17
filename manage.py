import os
#from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell, Server
from yammer_rank import create_app

config_name = os.getenv('FLASK_CONFIG')
print("manage.py, config_name: {}".format(config_name))
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
#migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))
#manager.add_command("db", MigrateCommand)

manager.add_command("runserver",
        Server(host="127.0.0.1", port=5000, use_debugger=True))

@manager.command
def test():
    """run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()