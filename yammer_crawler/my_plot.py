#!/usr/bin/env python


'''
Use matplotlib to draw  figures of  post and updates points
'''

# for MacOS
import matplotlib
matplotlib.use('TkAgg')
# for MacOS

import matplotlib.pyplot as plt
import numpy as np
import os
#from adjustText import adjust_text

from matplotlib import cbook
from matplotlib.cbook import get_sample_data

#import matplotlib
#matplotlib.use('Agg')

SAVE_PATH = os.path.join(os.getcwd(),'static')


def get_text_positions(text, x_data, y_data, txt_width, txt_height):
    a = zip(y_data, x_data)
    text_positions = list(y_data)
    for index, (y, x) in enumerate(a):
        local_text_positions = [i for i in a if i[0] > (y - txt_height)
                            and (abs(i[1] - x) < txt_width * 2) and i != (y,x)]
        if local_text_positions:
            sorted_ltp = sorted(local_text_positions)
            if abs(sorted_ltp[0][0] - y) < txt_height: #True == collision
                differ = np.diff(sorted_ltp, axis=0)
                a[index] = (sorted_ltp[-1][0] + txt_height, a[index][1])
                text_positions[index] = sorted_ltp[-1][0] + txt_height*1.01
                for k, (j, m) in enumerate(differ):
                    #j is the vertical distance between words
                    if j > txt_height * 2: #if True then room to fit a word in
                        a[index] = (sorted_ltp[k][0] + txt_height, a[index][1])
                        text_positions[index] = sorted_ltp[k][0] + txt_height
                        break
    return text_positions

def text_plotter(text, x_data, y_data, text_positions, txt_width,txt_height, final_num):
    n = 0
    for z,x,y,t in zip(text, x_data, y_data, text_positions):
        #print("x: {}, y: {}".format(x,y))
        color = 'black'
        if x >= final_num:
            color = 'r'
        n += 1
        font_size = 8
        if n <= 3:
            font_size= 9
        plt.annotate(str(z), xy=(x-txt_width/2, t), size=font_size, color=color)
        if y != t:
            '''
            plt.arrow(x, t,0,y-t, color='red',alpha=0.3, width=txt_width*0.1,
                head_width=txt_width, head_length=txt_height*0.5,
                zorder=0,length_includes_head=True)
            '''
            plt.arrow(x, t,0,y-t, color='black',alpha=0.2, width=0.001,
                      head_width=0.2, head_length=0.1,
                      zorder=0,length_includes_head=False)
            pass



def draw_figure(data_list, threshold, date_end, date_start, final_comment_number, show_top=10, group_name=None):
    '''

    :param data_list: [[id,name,updates,posts,photo],...]
    :param threshold: in fact it is no usage since the data_list has been filtered already
    :param date_end:
    :param date_start:
    :return:
    '''

    if (data_list) == None:
        print("Nothing")
        return

    final_comment_number = int(final_comment_number)
    show_top = int(show_top)
    print("DEBUG start draw_figure")
    if date_start == None:
        date_start = "beginning"
    if date_end == None:
        date_end = "Now"

    post_list= [x[3] for x in data_list if x[2]>threshold or x[3]>threshold]
    comment_list = [x[2] for x in data_list if x[2]>threshold or x[3]>threshold]
    name_list = [x[1] for x in data_list if x[2]>threshold or x[3]>threshold]
    photo_list= [x[-1] for x in data_list if x[2]>threshold or x[3]>threshold]

    max_x_value = max(comment_list)
    if final_comment_number < max_x_value:
        max_x_tick = max_x_value + 20
    else:
        max_x_tick = final_comment_number + 20

    print("start color")
    color = np.arctan2(post_list, comment_list)
    print("DEBUG color: {}".format(color))

    print("start plt.figure with plt id:{}".format(id(plt)))
    #fig= plt.figure(figsize=(8.0, 5.0))
    #Set fig size/resolution
    fig= plt.figure(figsize=(11.0, 7.5))

    print("start fig.add_subplot")
    ax1 = fig.add_subplot(111)


    s = ''
    if group_name != None:
        s = "Comments&Posts of {} \n(from {} to {})".format(group_name, date_end, date_start)
    else:
        s = "Comments&Posts (from {} to {})".format(date_end, date_start)
    title_str = s
    ax1.set_title(title_str, fontsize=18)
    plt.ylabel("Posts", fontsize=12)
    plt.xlabel("Comments", fontsize=12)
    max_y = 100
    max_x = 100
    if post_list:
        max_y = max(post_list)
    if comment_list:
        max_x = max(comment_list)

    #final_comment_number = 40
    plt.yticks([n for n in range(max_y + 20) if n % 5 == 0])
    plt.xticks([n for n in range(max_x_tick) if n % 5 == 0])
    plt.ylim(-5, max_y+25)
    #plt.xlim(-5, max_x+25)
    plt.xlim(-5, max_x_tick)

    print("Start to scatter")
    p_scatter = ax1.scatter(comment_list, post_list, s=500, c = color, alpha=0.5, marker='o', cmap=plt.get_cmap("Spectral"))

    y = [i for i in range(max(post_list)+20)]
    x = [final_comment_number for i in range(len(y))]
    #Draw the final line
    ax1.plot(x, y, '--', alpha=0.4)
    #ax1.text(x[0], y[0], 'The Final Line', ha='left', va='bottom', fontsize=10)
    ax1.text(x[-1], y[-1], 'The Finish Line~', ha='left', va='top', fontsize=10)
    #ax1.grid(True)

    labels = []
    ann = []
    for i in range(len(name_list)):

        label = ("%d. "%(i+1) + name_list[i] + "(%d,%d)"%(comment_list[i],post_list[i]))
        labels.append(label)

    txt_height = 0.0224 * (plt.ylim()[1] - plt.ylim()[0])
    txt_width = 0.045 * (plt.xlim()[1] - plt.xlim()[0])
    print("DEBUG plt.ylim()[1]: {}".format(plt.ylim()[1]))
    print("DEBUG plt.ylim()[0]: {}".format(plt.ylim()[0]))
    print("DEBUG plt.xlim()[1]: {}".format(plt.xlim()[1]))
    print("DEBUG plt.xlim()[0]: {}".format(plt.xlim()[0]))
    #txt_height = 0.51
    #txt_width = 5
    text_positions = get_text_positions(labels, comment_list, post_list, txt_width, txt_height)
    if show_top >= 0:
        text_plotter(labels[:show_top], comment_list[:show_top], post_list[:show_top], text_positions, txt_width, txt_height, final_comment_number)
    else:
        text_plotter(labels[show_top:], comment_list[show_top:], post_list[show_top:], text_positions, txt_width, txt_height, final_comment_number)

    #Delete right and top spines
    ax1.spines['top'].set_color('none')
    ax1.spines['right'].set_color('none')

    print("Return plt, id: {}".format(id(plt)))

    return plt
################draw_figure()##################################################################


if __name__ == '__main__':

    example_list = [[1639993032, u'LI Ellen', 54, 87, u'https://mug0.assets-yammer.com/mugshot/images/48x48/5h0BJ82WH7kQHlN3HJVbnrXTSMPBTfP1'],
[1639849062, u'MAI Maggie', 15, 24, u'https://mug0.assets-yammer.com/mugshot/images/48x48/nbJkD-pZVvtD9WmNlgHzRxmsDj83glHw'],
[1640337160, u'LIU Aaron', 7, 3, u'https://mug0.assets-yammer.com/mugshot/images/48x48/mbLFljlLhwkq2LttSJVn5C6TQpK01dnq'],
[1639911169, 'unknown user', 6, 1, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1639869576, u'LI Xin', 5, 31, u'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1642625168, u'LIU Albert', 5, 6, u'https://mug0.assets-yammer.com/mugshot/images/48x48/SQcJk93P3S8VWH6TSXSBTX2mfzN8QzC4'],
[1640005660, u'CHEN Chris', 4, 2, u'https://mug0.assets-yammer.com/mugshot/images/48x48/PrBm7gfNwNF5CgRrGpqgx8bP9wPJQMxq'],
[1610777031, u'XIE Crystal', 3, 4, u'https://mug0.assets-yammer.com/mugshot/images/48x48/hR45kTbX48WXnxJFK4JKDgXtKZ2hvRLq'],
[1640229078, u'YAN Tim', 3, 0, u'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1639997404, u'YANG Ellen', 3, 6, u'https://mug0.assets-yammer.com/mugshot/images/48x48/dHF8k13FKzdj3H8cxtGCt1GrtGfNNB0n'],
[1640229073, 'unknown user', 3, 3, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1568965136, 'unknown user', 2, 0, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1641702550, u'ZHANG Vicky', 2, 10, u'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1606014178, 'unknown user', 2, 0, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1538182089, 'unknown user', 2, 0, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1540232816, 'unknown user', 2, 0, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1640004140, u'ZHAO Joshua', 2, 0, u'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png'],
[1569252594, 'unknown user', 1, 0, 'https://mug0.assets-yammer.com/mugshot/images/48x48/no_photo.png']]


    group_name = "Qingdao Center"


    threshold = 0
    date_start = None
    date_end = None
    final_comment_number = 40
    show_top = 5
    plt =  draw_figure(example_list, threshold, date_end, date_start, final_comment_number, show_top, group_name)
    plt.show()
    #plt.savefig("test.png", dpi=200)

    print("Done")