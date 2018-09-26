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

@auth_bp.app_errorhandler(404)
def page_not_found(e):
    #return render_template('404.html'),404
    return 'auth_bp, 404.html',404


@auth_bp.app_errorhandler(500)
def internal_server_error(e):
    #return render_template('500.html'),500
    return 'auth_bp, 500.html',500