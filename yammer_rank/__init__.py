from flask import Flask
from config import my_config
from config import Config
from flask_oauthlib.client import OAuth
from . import my_constants

from celery import Celery


oauth = OAuth()
yammer_rank_oauth = oauth.remote_app(
    'Yammer Rank',
    consumer_key=my_constants.CLIENT_ID,
    consumer_secret=my_constants.CLIENT_SECRET,
    base_url='https://www.yammer.com/oauth2/authorize',
    request_token_url=None,
    #request_token_params={'scope': 'get_user_info'},
    request_token_params=None,
    access_token_url='https://www.yammer.com/oauth2/access_token'
    #authorize_url= my_constants.AUTH_URL
)

#celery
'''
my_celery = Celery(__name__,
                   broker=Config.CELERY_BROKER_URL,
                   backend=Config.CELERY_RESULT_BACKEND)
'''

def create_app(config_name):
    app = Flask(__name__)
    #print("DEBUG __name__ :{}".format(__name__))
    print("DEBUG Flask app created at yammer_rank/__init__.py,  __name__: {}".format(__name__))
    #print("DEBUG app.name: {}".format(app.name))
    app.config.from_object(my_config[config_name])

    my_config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    #oauth authentication
    oauth.init_app(app)

    #my_celery.conf.update(app.config)


    return app