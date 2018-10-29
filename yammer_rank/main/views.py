#!/usr/bin/env python
#coding=utf-8

'''
This is for the webpage
'''

from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect, url_for
from flask import jsonify

from datetime import datetime
import time
import os
import yampy
import json

from . import main
from .. import my_yammer
from .. import my_plot
from .. import my_constants
from yammer_rank import yammer_rank_oauth

# Use Celery
#from yammer_rank import my_celery

#app = Flask(__name__)
#app.config['SECRET_KEY'] = os.urandom(24)


'''
@my_celery.task
def long_time_task(ya, group_id, letter_num, least_comment_num, end_date, start_date, rank_for_post):
    print("DEBUG this is Celery function!!!!!!!")
    result = ya.get_group_rank(group_id, letter_num, least_comment_num, \
                                      end_date, start_date, rank_for_post)
    print("DEBUG celery function finished!!!!")
    return result
'''


@main.route('/')
def index():

    '''
    how to add token to a session?
    index -> (login) -> yammer_rank -> rank_result
    '''

    print("DEBUG this is / index function")
    if "access_token" in session:
        print("DEBUG already has the token")
        if not "user_name" in session:
            print("but no user_name")
            session["user_name"] = "local test"
        return redirect(url_for('main.yammer_rank'))

    elif my_constants.ACCESS_TOKEN:
        #local test mode
        #never set ACCESS_TOKEN in a production environment
        access_token = my_constants.ACCESS_TOKEN
        print("DEBUG local test envrionmeent has the TOKEN: {}".format(access_token))
        session["access_token"] = access_token
        session["user_name"] = "local test"
        print("DEBUG set user name local test")
        return render_template('main/yammer_rank.html', user_name="local test")
    else:
        pass
        #return "No token in session"

    #response from oauth_login callback
    #Yammer api doesn't allow /callback
    #see https://developer.yammer.com/docs/authentication-1
    resp = yammer_rank_oauth.authorized_response()
    print("DEBUG resp: {}".format(resp))

    if resp is not None:
        print("DEBUG this is main.index authorized function!!!!!!!!!!!!!!")
        print("DEBUG resp is not NONE!")
        print("DEBUG resp: {}, type(resp): {}".format(resp, type(resp)))
        #The key in resp is a dict contain access_token
        l_k = []
        for k in resp.keys():
            l_k.append(k)

        d_resp = json.loads(l_k[0])
        access_token = d_resp["access_token"]["token"]
        print("DEBUG access_token got: {}".format(access_token))
        if access_token == None:
            return "Login failed via oauth"

        user_name = d_resp["user"]["full_name"]
        user_name = user_name.split(",")[0] + " " + user_name.split(",")[1].split()[0]
        user_id = d_resp["user"]["id"]
        session["user_name"] = user_name
        session["id"] = user_id
        session["access_token"] = access_token
        session.permanent = True
        print("DEBUG token has been sessioned!")
        return redirect(url_for('main.yammer_rank'))

    print("DEBUG show index page since you need to click start to login")
    return render_template('main/index.html')


@main.route('/yammer_rank', methods=["POST", "GET"])
def yammer_rank():
    '''
    Input param to show rankings
    '''
    print("DEBUG this is yammer_rank()")
    #print("DEBUGGGGGGGG request.url: {}".format(request.url))
    #print("DEBUGGGGGGGG request.method: {}".format(request.method))
    #code = request.args.get("code")
    #print("DEBUG code: {}".format(code))

    access_token = session["access_token"]
    if not access_token:
        print("DEBUG invalid token")
        return ("Invalid token: {}".format(access_token))
    else:
        print("DEBUG yammer_rank get the toke: {}".format(access_token))

    user_name = session["user_name"]

    return render_template("main/yammer_rank.html", user_name=user_name)


#return the rank page!
@main.route('/rank_result', methods=['POST', 'GET'])
def get_rank_result():

    print("DEBUG this is get_rank_result view fuction")
    end_date = None
    start_date = None
    letter_num = 1
    least_comment_num = 1
    final_comment_num = 50
    show_top = 10
    group_id = '15273590'
    rank_for_post = False
    #The final rankings
    yammer_result = None
    total_comments = 0
    total_posts = 0
    access_token = session["access_token"]
    if not access_token:
        print("login expired, need to login first")
        return "Login needed"

    if request.method == 'POST':
        # yammer_result = ["a", "b", "c"]
        #str_now = datetime.now().strftime("%Y/%m/%d")
        end_date = request.form['end_date']
        start_date = request.form['start_date']
        letter_num  = request.form['letter_num']
        least_comment_num = request.form['least_comment_num']
        final_comment_num = request.form['final_comment_num']
        show_top = request.form['show_top']
        group_id = request.form['sel_group']
        #check group id validation
        print("DEBUG you input group_id :{}".format(group_id))


        rank_for_post = int(request.form['rank_for_post'])
        if rank_for_post == 0:
            rank_for_post = False
        else:
            rank_for_post = True


        if letter_num.isdigit():
            letter_num = int(letter_num)
        else:
            print("DEBUG no digit type!")
            letter_num = 1

        if least_comment_num.isdigit():
            least_comment_num = int(least_comment_num)
        else:
            least_comment_num = 1

        if start_date == "":
            start_date = None
        else:
            start_date = start_date.replace('-','/')

        if end_date == "":
            end_date = None
        else:
            end_date = end_date.replace('-','/')

    if request.method == 'GET':
        print("DEBUG GET rank_result")
        end_date = None
        start_date = None
        letter_num  = 1
        least_comment_num = 1
        final_comment_num = 50
        show_top = 10

    # Get the group messages and users
    # if there is in db, then direct get data from db
    # if there is not fresh data in db, then start the crawler

    # group_id = 15273590
    # group_id = 12562314
    ya = my_yammer.My_Yammer(access_token)
    group_name = ya.pull_group_name(group_id)
    if group_name == None:
        #wrong group id
        #alert(invalid group id)
        return "Invalid group id"
    else:

        #if new user, refresh the db user info
        #pass

        if yammer_result == None:
            yammer_result, total_comments, total_posts = ya.get_group_rank(group_id, letter_num, least_comment_num, \
                                               end_date, start_date, rank_for_post)
        # use celery
        '''
        print("DEBUG Start to call the long_time_task va celery")
        yammer_result = long_time_task.delay(ya, group_id, letter_num, least_comment_num, \
                                       end_date, start_date, rank_for_post)
        '''

    if yammer_result == None:
        print("DEBUG None message data, perhaps wrong group id!")

    # return render_template('yammer_rank.html', mylist=yammer_result, img_name=img_url)
    print("DEBUG start to created png")
    # 转成图片的步骤
    # tkinter RuntimeError: main thread is not in main loop
    # here need another thread?
    plt = my_plot.draw_figure(yammer_result, 0, end_date, start_date, final_comment_num, show_top, group_name, \
                              total_comments, total_posts)
    print("DEBUG Get plt id: {}".format(id(plt)))

    if start_date == None:
        start_date = "the ever biggning"
    if end_date == None:
        end_date = "now"

    from io import BytesIO
    import base64

    sio = BytesIO()
    plt.savefig(sio, format='png', dpi=100)
    img_data = base64.b64encode(sio.getvalue()).decode()
    # plt.close()
    rank_category = "Comment"
    if rank_for_post:
        rank_category = "Post"

    return render_template('main/rank_result.html', mylist=yammer_result, img_data=img_data, rank_category=rank_category)


# ajax
@main.route('/process_ajax', methods=['POST'])
def process_ajax():
    print("DEBUG this is process_ajax called from  ajax!!!!")
    end_date = None
    start_date = None
    letter_num = 1
    least_comment_num = 1
    final_comment_num = 50
    show_top = 10
    group_id = '15273590'
    rank_for_post = False
    # The final rankings
    yammer_result = None
    total_comments = 0
    total_posts = 0
    access_token = session["access_token"]
    if not access_token:
        print("login expired, need to login first")
        return "Login needed"

    if request.method == 'POST':
        # yammer_result = ["a", "b", "c"]
        # str_now = datetime.now().strftime("%Y/%m/%d")
        end_date = request.form['end_date']
        start_date = request.form['start_date']
        letter_num = request.form['letter_num']
        least_comment_num = request.form['least_comment_num']
        final_comment_num = request.form['final_comment_num']
        show_top = request.form['show_top']
        group_id = request.form['sel_group']
        # check group id validation
        print("DEBUG you input group_id :{}".format(group_id))

        rank_for_post = int(request.form['rank_for_post'])
        if rank_for_post == 0:
            rank_for_post = False
        else:
            rank_for_post = True

        if letter_num.isdigit():
            letter_num = int(letter_num)
        else:
            print("DEBUG no digit type!")
            letter_num = 1

        if least_comment_num.isdigit():
            least_comment_num = int(least_comment_num)
        else:
            least_comment_num = 1

        if start_date == "":
            start_date = None
        else:
            start_date = start_date.replace('-', '/')

        if end_date == "":
            end_date = None
        else:
            end_date = end_date.replace('-', '/')

    if request.method == 'GET':
        print("DEBUG GET rank_result")
        end_date = None
        start_date = None
        letter_num = 1
        least_comment_num = 1
        final_comment_num = 50
        show_top = 10

    # Get the group messages and users
    # if there is in db, then direct get data from db
    # if there is not fresh data in db, then start the crawler

    # group_id = 15273590
    # group_id = 12562314
    ya = my_yammer.My_Yammer(access_token)
    group_name = ya.pull_group_name(group_id)
    if group_name == None:
        # wrong group id
        # alert(invalid group id)
        return "Invalid group id"
    else:

        # if new user, refresh the db user info
        # pass

        if yammer_result == None:
            yammer_result, total_comments, total_posts = ya.get_group_rank(group_id, letter_num, least_comment_num, \
                                                                           end_date, start_date, rank_for_post)
        # use celery
        '''
        print("DEBUG Start to call the long_time_task va celery")
        yammer_result = long_time_task.delay(ya, group_id, letter_num, least_comment_num, \
                                       end_date, start_date, rank_for_post)
        '''

    if yammer_result == None:
        print("DEBUG None message data, perhaps wrong group id!")

    # return render_template('yammer_rank.html', mylist=yammer_result, img_name=img_url)
    print("DEBUG start to created png")
    # 转成图片的步骤
    # tkinter RuntimeError: main thread is not in main loop
    # here need another thread?
    plt = my_plot.draw_figure(yammer_result, 0, end_date, start_date, final_comment_num, show_top, group_name, \
                              total_comments, total_posts)
    print("DEBUG Get plt id: {}".format(id(plt)))

    if start_date == None:
        start_date = "the ever biggning"
    if end_date == None:
        end_date = "now"

    from io import BytesIO
    import base64

    sio = BytesIO()
    plt.savefig(sio, format='png', dpi=100)
    img_data = base64.b64encode(sio.getvalue()).decode()
    print("DEBUG img_data: {}, isinstance(img_data, bytes): {}".format(img_data[:10], isinstance(img_data, bytes)))
    # plt.close()
    rank_category = "Comment"
    if rank_for_post:
        rank_category = "Post"

    response = {'group_id':group_id, 'group_name':group_name, 'yammer_result':yammer_result, 'img_data':img_data}
    print("DEBUG process_jax finished!!!!!!!!!!!")

    return jsonify(response), 200



if __name__ == '__main__':


    #app.run(debug=True)
    #manager.run()
    print("done")
