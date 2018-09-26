from flask import Flask, redirect, url_for, session, request, jsonify
from flask_oauthlib.client import OAuth


app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

github = oauth.remote_app(
    'github',
    consumer_key='b41BFW3YX3b3644ugrX51A',
    consumer_secret='Vh25FoxXvCznx2z9AC0StfBDt2dJ6cVasWPW1y7k',
    request_token_params={'scope': 'user:email'},
    base_url='https://www.yammer.com/api/v1',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://www.yammer.com/oauth2/access_token',
    authorize_url='https://www.yammer.com/oauth2/authorize'
)


@app.route('/')
def index():
    if 'github_token' in session:
        me = github.get('user')
        return jsonify(me.data)
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return github.authorize(callback='https://yammerrank.herokuapp.com')


@app.route('/logout')
def logout():
    session.pop('github_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason=%s error=%s resp=%s' % (
            request.args['error'],
            request.args['error_description'],
            resp
        )
    session['github_token'] = (resp['access_token'], '')
    me = github.get('user')
    return jsonify(me.data)


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


if __name__ == '__main__':
    app.run()