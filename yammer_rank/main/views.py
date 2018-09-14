#!/usr/bin/env python
#coding=utf-8

'''
This is for the webpage
'''

from flask import Flask
from flask import request
from flask import render_template
from flask import session

from datetime import datetime
import time
import os

from . import main
from .. import my_yammer
from .. import my_plot
from .. import my_constants

#app = Flask(__name__)
#app.config['SECRET_KEY'] = os.urandom(24)

'''
@main.route('/')
def index():

    if ACCESS_TOKEN == None:
        #need to login via oauth
        print("DEBUG ACCESS_TOKEN == NONE, need to login.")
        pass
    else:
        #Add token into the session
        print("ACCESS_TOKEN is existed.")
        pass

    ya = my_yammer.My_Yammer(ACCESS_TOKEN)
    groups = ya.get_groups()
    print("DEBUG groups: {}".format(groups))
    auth_url = \
        'https://www.yammer.com/dialog/oauth?client_id=2fxbPxiDYwtM40yN3m0fQ&redirect_uri=https%3A%2F%2Fyammerstate.herokuapp.com'
    #return auth_url
    return render_template('login.html', groups=groups)
'''

@main.route('/')
def index():

    '''
    how to add token to a session?
    index -> (login) -> yammer_rank -> rank_result
    '''
    return render_template('index.html')


def oauth_login():
    access_token = None
    auth_url = \
        'https://www.yammer.com/dialog/oauth?client_id=2fxbPxiDYwtM40yN3m0fQ&redirect_uri=https%3A%2F%2Fyammerstate.herokuapp.com'

    if my_constants.ACCESS_TOKEN == None:
        #need to login via oauth
        print("DEBUG ACCESS_TOKEN == NONE, need to login.")
        pass
    else:
        #Add token into the session
        print("ACCESS_TOKEN is existed.")
        pass

    ya = my_yammer.My_Yammer(my_constants.ACCESS_TOKEN)
    groups = ya.get_groups()
    print("DEBUG groups: {}".format(groups))
    #return auth_url

    return access_token


@main.route('/yammer_rank', methods=["POST"])
def yammer_rank():
    '''
    Input param to show rankings
    '''
    if not my_constants.ACCESS_TOKEN:
        if not session.get("user_id"):
            #login via oauth
            #ACCESS_TOKEN =
            pass


    ya = my_yammer.My_Yammer(my_constants.ACCESS_TOKEN)
    groups = ya.get_groups()
    user_name, user_id = ya.get_current_name_id()
    print("DEBUGGGGGGGGGGGGGGGG groups: {}".format(groups))
    session["user_name"] = user_name
    session["user_id"] = user_id
    session["access_token"] = my_constants.ACCESS_TOKEN
    session.permanent = True
    #return auth_url


    print("DEBUG you click the login button")

    return render_template("yammer_rank.html", user_name=user_name, groups=groups)





#return the rank page!
@main.route('/rank_result', methods=['POST', 'GET'])
def get_rank_result():

    end_date = None
    start_date = None
    letter_num = 1
    least_comment_num = 1
    final_comment_num = 50
    show_top = 10
    group_id = '15273590'
    rank_for_post = False

    if request.method == 'POST':
        # yammer_result = ["a", "b", "c"]
        #str_now = datetime.now().strftime("%Y/%m/%d")
        end_date = request.form['end_date']
        start_date = request.form['start_date']
        letter_num  = request.form['letter_num']
        least_comment_num = request.form['least_comment_num']
        final_comment_num = request.form['final_comment_num']
        show_top = request.form['show_top']

        print("DEBUG show_top: {}".format(show_top))
        group_id = request.form['sel_group']
        print("DEBUG group_id: {}".format(group_id))
        rank_for_post = int(request.form['rank_for_post'])
        if rank_for_post == 0:
            rank_for_post = False
        else:
            rank_for_post = True

        print("DEBUG group_id :{}".format(group_id))

        if letter_num.isdigit():
            letter_num = int(letter_num)
        else:
            print("no digit type!")
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
        print("GET rank_result")
        end_date = None
        start_date = None
        letter_num  = 1
        least_comment_num = 1
        final_comment_num = 50
        show_top = 10

    # group_id = 15273590
    # group_id = 12562314
    ya = my_yammer.My_Yammer(my_constants.ACCESS_TOKEN)
    group_name = ya.get_group_name(group_id)
    yammer_result = ya.get_group_rank(group_id, letter_num, least_comment_num,\
                                      end_date, start_date, rank_for_post)
    # return render_template('yammer_rank.html', mylist=yammer_result, img_name=img_url)
    print("DEBUG start to created png")
    # 转成图片的步骤
    # tkinter RuntimeError: main thread is not in main loop
    # here need another thread?
    plt = my_plot.draw_figure(yammer_result, 0, end_date, start_date, final_comment_num, show_top, group_name)
    print("Get plt id: {}".format(id(plt)))

    if start_date == None:
        start_date = "the ever biggning"
    if end_date == None:
        end_date = "now"

    from io import BytesIO
    import base64

    sio = BytesIO()
    plt.savefig(sio, format='png', dpi=100)
    data = base64.b64encode(sio.getvalue()).decode()
    # plt.close()
    rank_category = "Comment"
    if rank_for_post:
        rank_category = "Post"

    return render_template('rank_result.html', mylist=yammer_result, my_data=data, rank_category=rank_category)


if __name__ == '__main__':


    #app.run(debug=True)
    #manager.run()
    print("done")
