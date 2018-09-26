from flask import render_template, redirect, url_for, request, session
from . import auth_bp
import yampy
from .. import my_constants

from yammer_rank import oauth

yammer_rank_oauth = oauth.remote_app(
    'Yammer Rank',
    consumer_key=my_constants.CLIENT_ID,
    consumer_secret=my_constants.CLIENT_SECRET,
    base_url='https://api.yammer.com',
    request_token_url=None,
    request_token_params={'scope': 'get_user_info'},
    access_token_url='/oauth2.0/token',
    authorize_url= my_constants.AUTH_URL
)

@auth_bp.route('/oauth_login')
def oauth_login():

    print("DEBUG this is oauth_login")
    if "access_token" not in session:
        return yammer_rank_oauth.authorize(callback=url_for('auth.authorized', _external=False))
    else:
        return redirect(url_for('main.yammer_rank'))


@auth_bp.route('/authorized')
def authorized():
    resp = yammer_rank_oauth.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' %\
        (request.args['error_reason'], request.args['error_description'])
        
    access_token = (resp['access_token'], '')
    print("DEBUG access_token got: ".format(access_token))
    session['access_token'] = access_token

    # Get openid via access_token, openid and access_token are needed for API calls
    #resp = qq.get('/oauth2.0/me', {'access_token': session['qq_token'][0]})
    #resp = json_to_dict(resp.data)
    #if isinstance(resp, dict):
    #    session['qq_openid'] = resp.get('openid')
    if access_token == None:
        return "Login failed via oauth"
    else:
        return redirect(url_for('main.yammer_rank'))


def get_access_token():
    access_token = None
    authenticator = yampy.Authenticator(client_id=my_constants.CLIENT_ID, client_secret=my_constants.CLIENT_SECRET)
    redirect_uri = my_constants.REDIRECT_URL
    auth_url = authenticator.authorization_url(redirect_uri=redirect_uri)

    #how to get the code?
    code = None
    access_token = authenticator.fetch_access_token(code)

    return access_token