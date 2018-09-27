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
import yampy

from . import main
from .. import my_yammer
from .. import my_plot
from .. import my_constants

#app = Flask(__name__)
#app.config['SECRET_KEY'] = os.urandom(24)

@main.route('/')
def index():

    '''
    how to add token to a session?
    index -> (login) -> yammer_rank -> rank_result
    '''
    code = request.args.get("code")
    print("DEBUG code: {}".format(code))

    if "access_token" in session:
        print("DEBUG already has the token")
        return render_template('main/yammer_rank.html')
        print("DEBUG initally, no token")
    else:
        return render_template('main/index.html')


@main.route('/yammer_rank', methods=["POST", "GET"])
def yammer_rank():
    '''
    Input param to show rankings
    '''
    print("DEBUGGGGGGGG request.url: {}".format(request.url))
    print("DEBUGGGGGGGG request.method: {}".format(request.method))

    code = request.args.get("code")
    print("DEBUG code: {}".format(code))

    if session["access_token"] == None:
        #No valid token, request return error login
        print("Invalid login")
        return ("login failed")


    access_token = session["access_token"]
    if not access_token:
        print("invalid token")
        return ("Invalid token: {}".format(access_token))
    else:
        print("DEBUG yammer_rank get the toke: {}".format(access_token))
    ya = my_yammer.My_Yammer(access_token)
    user_name, user_id = ya.get_current_user()

    session["user_name"] = user_name
    session["user_id"] = user_id
    #session["access_token"] = access_token
    session.permanent = True
    #return auth_url

    return render_template("main/yammer_rank.html", user_name=user_name)


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
    #The final rankings
    yammer_result = None
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

        yammer_result = ya.get_group_rank(group_id, letter_num, least_comment_num, \
                                          end_date, start_date, rank_for_post)


    if yammer_result == None:
        print("DEBUG None message data, perhaps wrong group id!")

    # return render_template('yammer_rank.html', mylist=yammer_result, img_name=img_url)
    print("DEBUG start to created png")
    # 转成图片的步骤
    # tkinter RuntimeError: main thread is not in main loop
    # here need another thread?
    plt = my_plot.draw_figure(yammer_result, 0, end_date, start_date, final_comment_num, show_top, group_name)
    print("DEBUG Get plt id: {}".format(id(plt)))

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

    return render_template('main/rank_result.html', mylist=yammer_result, my_data=data, rank_category=rank_category)


if __name__ == '__main__':


    #app.run(debug=True)
    #manager.run()
    print("done")
