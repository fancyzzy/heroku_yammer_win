from flask import Flask
from config import config


#print("yammer_rank/__init__.py, config: {}".format(config))

def create_app(config_name):
    app = Flask(__name__)
    print("DEBUG Flask app created at yammer_rank/__init__.py,  __name__: {}".format(__name__))
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app