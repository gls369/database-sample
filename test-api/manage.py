from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, Shell
from app import app, db
from models import Person



manager = Manager(app)

manager.add_command('db', MigrateCommand)

manager.add_command('runserver', Server(host = 'localhost', port = 5000))




def make_shell_context():
    return dict(app=app, db=db, Features=Features)

manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def rungevent():
    import werkzeug.serving
    from werkzeug.debug import DebuggedApplication
    from gevent.pywsgi import WSGIServer

    @werkzeug.serving.run_with_reloader
    def run():
        app.debug = True
        app = DebuggedApplication(app, evalex=True)
        ws = WSGIServer(('', 5000), app)
        ws.serve_forever()
        

    run()

if __name__ == '__main__':
    manager.run()

