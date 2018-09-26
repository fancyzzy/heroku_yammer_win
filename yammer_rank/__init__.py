from flask import Flask
from config import my_config
from flask_oauthlib.client import OAuth

oauth = OAuth()

#print("yammer_rank/__init__.py, config: {}".format(config))

def create_app(config_name):
    app = Flask(__name__)
    print("DEBUG Flask app created at yammer_rank/__init__.py,  __name__: {}".format(__name__))
    app.config.from_object(my_config[config_name])
    my_config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    #oauth authentication
    oauth.init_app(app)


    return app