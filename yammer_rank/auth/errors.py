#!/usr/bin/env python
#coding=utf-8

'''
This is for the webpage
'''

from flask import Flask
from flask import request
from flask import make_response
from flask import redirect
from flask import abort

from flask import render_template
from . import auth_bp

from yammer_rank import yammer_rank_oauth
import yampy
from .. import my_constants

@auth_bp.app_errorhandler(404)
def page_not_found(e):
    #return render_template('404.html'),404
    return 'auth_bp, 404.html',404


@auth_bp.app_errorhandler(500)
def internal_server_error(e):
    #return render_template('500.html'),500

    # response from oauth_login callback
    resp = yammer_rank_oauth.authorized_response()

    if resp is not None:
        print("DEBUG this is 500 error function!!!!!!!!!!!!!!")
        print("DEBUG resp: {}".format(resp))
        # how to get the code?
        authenticator = yampy.Authenticator(client_id=my_constants.CLIENT_ID, client_secret=my_constants.CLIENT_SECRET)
        redirect_uri = my_constants.REDIRECT_URL
        auth_url = authenticator.authorization_url(redirect_uri=redirect_uri)
        print("DEBUG auth_url: {}".format(auth_url))
        code = None
        code = request.args.get("code")
        print("DEBUG code: {}, type(code): {}".format(code, type(code)))
        access_token = authenticator.fetch_access_token(code)

        # access_token = (resp['access_token'], '')
        print("DEBUG access_token got: {}".format(access_token))

    return 'auth_bp, 500.html',500