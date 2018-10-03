from flask import render_template, redirect, url_for, request, session
from . import auth_bp
import yampy

from yammer_rank import oauth
from yammer_rank import yammer_rank_oauth
from .. import my_constants


@auth_bp.route('/oauth_login')
def oauth_login():

    #local test mode
    #never set ACCESS_TOKEN in a production environment
    if my_constants.ACCESS_TOKEN:
        access_token = my_constants.ACCESS_TOKEN
        print("DEBUG local envrionmeent has the TOKEN: {}".format(access_token))
        session["access_token"] = access_token
        return render_template('main/yammer_rank.html')


    print("DEBUG this is oauth_login")
    #return yammer_rank_oauth.authorize(callback=url_for('main.index', _external=True))
    return yammer_rank_oauth.authorize(callback=my_constants.REDIRECT_URL)


#Yammer api doesn't allow /callback
#see https://developer.yammer.com/docs/authentication-1

@auth_bp.route('/')
def authorized():
    print("DEBUG this is authorized function!!!!!!!!!!!!!!")
    resp = yammer_rank_oauth.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' %\
        (request.args['error_reason'], request.args['error_description'])
        
    access_token = (resp['access_token'], '')
    print("DEBUG access_token got: ".format(access_token))
    session['access_token'] = access_token
    print("DEBUG token has been sessioned!")

    # Get openid via access_token, openid and access_token are needed for API calls
    #resp = qq.get('/oauth2.0/me', {'access_token': session['qq_token'][0]})
    #resp = json_to_dict(resp.data)
    #if isinstance(resp, dict):
    #    session['qq_openid'] = resp.get('openid')
    if access_token == None:
        return "Login failed via oauth"
    else:
        return redirect(url_for('main.yammer_rank'))
