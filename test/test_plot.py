#!/usr/bin/env
import my_plot
from flask import send_file

#import matplotlib
# matplotlib.use('Agg')
#import matplotlib.pyplot as plt
from io import BytesIO
import base64
import my_yammer


def send_data():
    ya = my_yammer.My_Yammer()
    group_id = '15273590'
    #group_id = '12562314'
    letter_num = 1
    end_date = None
    start_date = None
    least_comment_num = 1
    yammer_result = ya.get_group_rank(group_id, letter_num, least_comment_num, end_date, start_date)

    print("DEBUG start to created png")
    total_line = 100
    plt =  my_plot.draw_figure(yammer_result, 0, end_date, start_date, total_line)
    print("Get plt id: {}".format(id(plt)))


    if start_date == None:
        start_date = "the ever biggning"
    if end_date == None:
        end_date = "now"

    sio = BytesIO()
    if plt == None:
        return

    plt.savefig(sio, format='png', dpi=100)
    data = base64.b64encode(sio.getvalue()).decode()
    plt.close()

    print("done")


if __name__ == '__main__':
    print("###############1st#############")
    send_data()
    print("###############2nd#############")
    send_data()
    print("###############3rd#############")
    send_data()
    print("###############4th#############")
    send_data()
    print("###############4th#############")
    send_data()
    print("###############4th#############")
    send_data()
    print("###############4th#############")
    send_data()
    print("###############4th#############")
    send_data()


