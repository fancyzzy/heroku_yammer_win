#!/usr/bin/env python

'''
Crawl yammer message info
by RESful API:
https://www.yammer.com/api/v1/messages/in_group/15273590.json

Method:
Use yampy to download json data
'''

import json
import yampy
from yampy import errors

import time



BASE_API = 'http://www.yammer.com/api/v1'
#YAMMER_API_MESSAGE = 'https://www.yammer.com/api/v1/messages/in_group/15273590.json'
YAMMER_GROUP_MESSAGES = 'https://www.yammer.com/api/v1/messages/in_group/'
#YAMMER_API_USER = 'https://www.yammer.com/api/v1/users/in_group/15273590.json'

YAMMER_GROUP_USERS = 'https://www.yammer.com/api/v1/users/in_group/'

API_RESTRICT = 20

#MY_CLIENT_ID = '2fxbPxiDYwtM40yN3m0fQ'
#MY_CLIENT_SECRET = 'hJKivZUnqsl6vAP2NyaFodWK2nNDxHJ5MxwPtg4s'
#REDIRECT_URI = 'https://yammerrank.herokuapp.com'


def extend_diff(list_source, list_new):
    for item in list_new:
        if item not in list_source:
            list_source.append(item)
###############extend_diff()#############################

from types import  MethodType
def from_group(self, group_id, older_than=None, newer_than=None,
               limit=None, threaded=None):
    """

    Returns messages that were posted in the group identified by group_id.

    See the :meth:`all` method for a description of the keyword arguments.

    param group_id is int !

    """
    path = "/messages/in_group/%d" % (group_id)
    return self._client.get(path, **self._argument_converter(
        older_than=older_than,
        newer_than=newer_than,
        limit=limit,
        threaded=threaded,
        ))


class My_Crawler():
    def __init__(self, access_token=None):

        '''
        authenticator = yampy.Authenticator(client_id=MY_CLIENT_ID, client_secret=MY_CLIENT_SECRET)
        auth_url = authenticator.authorization_url(redirect_uri=REDIRECT_URI)
        print("Debug auth_url: {}".format(auth_url))

        auth_url = \
        'https://www.yammer.com/dialog/oauth?client_id=2fxbPxiDYwtM40yN3m0fQ&redirect_uri=https%3A%2F%2Fyammerstate.herokuapp.com'

        code = "xMK0kj1bGHmCp6gELwX44Q"

        access_data = authenticator.fetch_access_data(code)

        access_token = access_data.access_token.token
        print("DEBUG access_token: {}".format(access_token))
        '''

        if access_token == None:
            print("DEBUG My_Crawler, token = None")
            return

        self.yampy = yampy.Yammer(access_token=access_token)
        self.user_info = self.yampy.users.find_current()
        #print("DEBUG self. user_info: {}".format(self.user_info))

        #dynamicly add method
        self.yampy.messages.from_group = MethodType(from_group, self.yampy.messages)


        print("DEBUG My crawler init finished")

    ############__init__()##############


    def get_group_name(self, group_id):
        '''
        get group name from the message dict
        :param group_id:
        :return:
        '''

        group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id)
        print("DEBUG Check group name in 'meta','feed_name' of {}".format(group_messages_url))

        # Call yampy API
        try:
            json_dict = self.yampy.messages.from_group(int(group_id))
        except errors.NotFoundError:
            print("DEBUG group messages not found via this group id")
            return None

        if json_dict != None:
            if "feed_name" in json_dict["meta"].keys():
                group_name = json_dict["meta"]["feed_name"]
                return group_name
            else:
                return None
        else:
            return None
    ##########get_group_name()#####################


    def download_all_messages(self, group_id, interval=1, older_than_message_id=None, n=None):
        '''

        download all the messages in the group
        continue to download until no new messages
        as one time only 20 messages allowed
        :param group_id: string, yammer group id
        :param interval: download interval
        :param older_than_message_id: only download older messages than this
        :param n: download times
        :return: json liked dict
        '''

        print("DEBUG Start download all messages")
        json_result = None
        json_str = None
        i = 0
        #YAMMER_API_MESSAGE = 'https://www.yammer.com/api/v1/messages/in_group/'
        group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id)
        if older_than_message_id != None:
            group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + '?older_than=%s'%(older_than_message_id)

        while 1:
            i += 1
            print("DEBUG Download batch {}".format(i))
            print("DEBUG url: {}".format(group_messages_url))

            #Call yampy API
            json_dict = self.yampy.messages.from_group(int(group_id), older_than_message_id)

            #concatenate json_str to json_result
            if json_result == None:
                json_result = json_dict
            else:
                if "messages" in json_dict.keys():
                    json_result["messages"].extend(json_dict["messages"])
                else:
                    print("DEBUG Error, there is no message key!")
                    break

                if "feferences" in json_dict.keys():
                    extend_diff(json_result["references"], json_dict["references"])
                if "followed_user_ids" in json_dict["meta"].keys():
                    extend_diff(json_result["meta"]["followed_user_ids"], json_dict["meta"]["followed_user_ids"])
                if "followed_references" in json_dict["meta"].keys():
                    extend_diff(json_result["meta"]["followed_references"], json_dict["meta"]["followed_references"])

            # Check to continue
            if json_dict["meta"]["older_available"]:
                print("DEBUG older available, sleep %d second.."%(interval))
                time.sleep(interval)
                older_than_message_id = json_dict["messages"][-1]["id"]
                group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + \
                                     '?older_than=%s'%(older_than_message_id)
            else:
                print("DEBUG No more messages, download finished")
                break

            if n and i >= n:
                print("DEBUG Stop download by %d times"%(n))
                break

        return json_result

    ###########download_all_messages()###################################################


    def download_newer_messages(self, group_id, newer_than_message_id, interval=1):
        '''
        Download newer messages based on the existing database

        :param group_id:
        :param newer_than_message_id:
        :return: newer_json_result
        '''

        print("DEBUG Start download newer messages than %s"%(newer_than_message_id))
        newer_json_result = None
        json_str = None
        i = 0
        #YAMMER_API_MESSAGE = 'https://www.yammer.com/api/v1/messages/in_group/'
        group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + '?newer_than=%s'%(newer_than_message_id)

        older_than_message_id = None

        while 1:
            i += 1
            print("DEBUG Download batch {}".format(i))
            print("DEBUG url: {}".format(group_messages_url))

            #Call yampy API
            if not older_than_message_id:
                json_dict = self.yampy.messages.from_group(int(group_id), None, newer_than_message_id)
            else:
                json_dict = self.yampy.messages.from_group(int(group_id), older_than_message_id)

            #print("DEBUG json_dict: {}".format(json_dict))
            if len(json_dict["messages"]) == 0:
                print("DEBUG No new messages found.")
                break

            #concatenate json_str to newer_json_result
            if newer_json_result == None:
                newer_json_result = json_dict
            else:
                #May have same messages
                extend_diff(newer_json_result["messages"], json_dict["messages"])

                if "references" in json_dict.keys():
                    extend_diff(newer_json_result["references"], json_dict["references"])

                if "followed_user_ids" in json_dict["meta"].keys():
                    extend_diff(newer_json_result["meta"]["followed_user_ids"], json_dict["meta"]["followed_user_ids"])

                if "followed_references" in json_dict["meta"].keys():
                    extend_diff(newer_json_result["meta"]["followed_references"], json_dict["meta"]["followed_references"])

            # Check to stop, if < 20 means download complete
            if len(json_dict["messages"]) < API_RESTRICT:
                print("DEBUG No more newer messages, download finished")
                break
            else:
                for message_dict in json_dict["messages"]:
                    if message_dict["id"] == newer_than_message_id:
                        print("DEBUG No more newer messages, download finished")
                        break

            print("DEBUG more newer messages available, sleep %d second.."%(interval))
            time.sleep(interval)
            older_than_message_id = json_dict["messages"][-1]["id"]
            group_messages_url = YAMMER_GROUP_MESSAGES + '%s.json'%(group_id) + \
                                 '?older_than=%s'%(older_than_message_id)

        return newer_json_result
    ###########################download_newer_messages()##########################################


    def get_latest_message(self, group_id, json_data):
        '''
        :param group_id:
        :param json_data:
        :return: message_id str
        '''
        message_id = ''

        return json_data["messages"][0]["id"]
    ##########get_latest_message#########################################################


    def get_oldest_message(self, group_id, json_data):
        '''
        :param group_id:
        :param json_data:
        :return: message_id str
        '''
        message_id = ''

        return json_data["messages"][-1]["id"]
    #############get_oldest_message()####################################################


    def download_all_users(self, group_id, interval=5):
        '''

        download all the users in the group
        :param group_id: string, yammer group id
        :param interval: download interval
        :return: json liked dict see:
        https://www.yammer.com/api/v1/users/in_group/15273590.json
        '''
        print("DEBUG Start download all users")

        json_result = None
        json_str = None
        i = 0
        page_num = 0
        #YAMMER_GROUP_USER = 'https://www.yammer.com/api/v1/users/in_group/'
        group_users_url = YAMMER_GROUP_USERS  + '%s.json'%(group_id)

        while 1:
            i += 1
            print("DEBUG Download batch {}".format(i))
            print("DEBUG url: {}".format(group_users_url))

            #Call yampy API
            json_dict = self.yampy.users.in_group(int(group_id), page_num)

            #concatenate json_str to json_result
            if json_result == None:
                json_result = json_dict
            else:
                if len(json_dict["users"]) != 0:
                    json_result["users"].extend(json_dict["users"])

                    extend_diff(json_result["meta"]["followed_user_ids"], json_dict["meta"]["followed_user_ids"])
                else:
                    print("DEBUG Can't find more users due to yammer api bug")
                    break

            # Check to continue
            if json_dict["more_available"]:
                print("DEBUG more available, sleep %d second.."%(interval))
                time.sleep(interval)

                page_num = i+1
                group_users_url = YAMMER_GROUP_USERS + '%s.json'%(group_id) + '?page=%d'%(page_num)
            else:
                print("DEBUG No more users, download finished")
                break

        return json_result

    ###########download_all_users()###################################################


    def download_user_details(self, user_dict, interval=1):
        '''
        download one user detailed information from the url in the user dict

        :param user_dict: Contatins all user info in key 'url' value
        see: https://www.yammer.com/api/v1/users/1640338967.json
        :return: details of all users in this group as json files for each user
        '''

        full_name = ''
        job_title = ''
        state = '' #if this id is still available
        user_url = user_dict["url"] + '.json'
        user_name = user_dict["full_name"]
        print("DEBUG Start download user detail of {}".format(user_name))
        print("DEBUG url: {}".format(user_url))
        json_str = None

        #Call yampy API
        api_str = user_url.replace(BASE_API, '')
        print("DEBUG api_str: {}".format(api_str))
        json_dict = self.yampy.client.get(api_str)

        time.sleep(interval)
        return json_dict

    ###########download_user_details()############################################


    def find_user_url(self, user_id):

        web_url = None
        try:
            web_url = self.yampy.users.find(user_id)["web_url"]
        except Exception as e:
            print("DEBUG no such user, error: {}".format(e))
            return None
        return web_url
    ################find_user()##################################################


if __name__ == '__main__':

    group_id = 12562314 #Qingdao
    group_id = 15273590 #English group
    #access_token = '592-FnmLDb1cF0zMgyj32jnz0w'

    from my_constants import ACCESS_TOKEN
    my_crawler = My_Crawler(ACCESS_TOKEN)

    '''
    #test download and save all messages in the group
    result_json = my_crawler.download_all_messages(group_id, interval=1, older_than_message_id=None, n=None)
    print("Debug messages number: {}, result_json: {}".format(len(result_json["messages"]), result_json))
    file_name = 'group_%s_messages.json'%(group_id)
    with open(file_name, 'w') as fb:
        #convert dict to string
        fb.write(json.dumps(result_json))
    '''


    #test download and save all users in the group

    '''
    result_json = my_crawler.download_all_users(int(group_id), interval=1)
    print("Debug users number: {}, result_json: {}".format(len(result_json["users"]), result_json))
    '''

    #Test to download newer messages
    newer_than_message_id = '1147793449'
    newer_result_json = my_crawler.download_newer_messages(group_id, newer_than_message_id, interval=1)
    if newer_result_json:
        print("DEBUG new message num: {}, newer_result_json: {}".\
     format(len(newer_result_json["messages"]), newer_result_json))
    else:
        print("None newer messages")


    user_id = 1538316736
    user_url = my_crawler.find_user_url(user_id)
    print("DEBUG web_url: {}".format(user_url))




    print("done")





