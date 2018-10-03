from flask import render_template, redirect, url_for, request, session
from . import auth_bp
import yampy

from yammer_rank import oauth
from yammer_rank import yammer_rank_oauth
from .. import my_constants


@auth_bp.route('/oauth_login')
def oauth_login():

    print("DEBUG this is oauth_login")


    #return yammer_rank_oauth.authorize(callback=url_for('main.index', _external=True))
    return yammer_rank_oauth.authorize(callback=my_constants.REDIRECT_URL)
