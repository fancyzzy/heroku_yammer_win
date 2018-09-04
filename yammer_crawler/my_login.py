#!/usr/bin/env python
#coding=utf-8

'''
This is for the webpage
'''

from flask import Flask, redirect, url_for, session, request, jsonify
from flask import render_template

from flask_oauthlib.client import OAuth
import my_yammer

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
app.config['DEBUG'] = True
oauth = OAuth(app)

github = oauth.remote_app(
    'github',
    consumer_key='2fxbPxiDYwtM40yN3m0fQ',
    consumer_secret='hJKivZUnqsl6vAP2NyaFodWK2nNDxHJ5MxwPtg4s',
    request_token_params=None,
    base_url='https://api.yammer.com/',
    request_token_url=None,
    access_token_method='POST',
    #access_token_url='https://yammer.com/login/oauth/access_token',
    access_token_url=None,
    #authorize_url='https://www.yammer.com/dialog/oauth?redirect_uri=https%3A%2F%2Fyammerstate.herokuapp.com'
    authorize_url='https://www.yammer.com/dialog/oauth?client_id=2fxbPxiDYwtM40yN3m0fQ&redirect_uri=https%3A%2F%2Fyammerstate.herokuapp.com'
)


@app.route('/')
def index():
    if 'github_token' in session:
        me = github.get('user')
        return jsonify(me.data)
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    print("DEBUGGGG authorized!!!!")
    resp = github.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['github_token'] = (resp['access_token'], '')
    me = github.get('user')
    #return jsonify(me.data)

    ya = my_yammer.My_Yammer()
    groups = ya.get_groups()
    print("DEBUG groups: {}".format(groups))
    return render_template('login.html', groups=groups)


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


if __name__ == '__main__':
    app.run(debug=True)
