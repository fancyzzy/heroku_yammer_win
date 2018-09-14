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
#!/usr/bin/env python3

from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    #return render_template('404.html'),404
    return '404.html',404


@main.app_errorhandler(500)
def internal_server_error(e):
    #return render_template('500.html'),500
    return '500.html',500