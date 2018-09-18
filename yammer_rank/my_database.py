#!/usr/bin/env python

'''
Crawl yammer then saved in the database
Use MongoDB
'''
import os
import json

DATA_PATH = os.path.join(os.getcwd(), 'data')
print("m_dtaba.py,  DATA_PATH: {}".format(DATA_PATH))
GROUP_DB = 'groups.json'
GROUP_DB_PATH = os.path.join(DATA_PATH, GROUP_DB)

class My_Database():
    def __init__(self):

        self.group_db = {}
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)

        for item in os.listdir(DATA_PATH):
            if item.endswith('.json'):
                self.group_db[item.split('_')[1]] = {"messages":None, "users":None}

        for item in os.listdir(DATA_PATH):
            if item.endswith('messages.json'):
                self.group_db[item.split('_')[1]]["messages"] = item
            elif item.endswith('users.json'):
                self.group_db[item.split('_')[1]]["users"] = item
            else:
                pass

        print("my database have group data: {}".format(self.group_db))

    #########__init__()######################################################

    def get_group_db(self):
        return self.group_db

    ############get_group_db()###############################################

    def get_group_name(self, group_id):

        existed_messages = self.get_group_messages(group_id)
        if existed_messages == None:
            print("Group data is not existed yet")
        else:
            return existed_messages["meta"]["feed_name"]
    ########get_group_name###########################################


    def get_all_groups_name_id(self):

        group_names = []
        for group_id in self.get_group_db().keys():
            group_name = self.get_group_name(group_id)
            group_names.append((group_name, group_id))

        return group_names
    ############get_downloaded_group_names()###########################



    def update_group_messages(self, exsited_data, newer_data, group_id):
        '''

        :param exsited_data:
        :param newer_data:
        :param group_id:
        :return: None
        '''

        #input to the head
        exsited_data["messages"][:0] = newer_data["messages"]
        if "references" in newer_data.keys():
            exsited_data["references"][:0] = newer_data["references"]
        if "followed_user_ids" in newer_data["meta"].keys():
            exsited_data["meta"]["followed_user_ids"][:0] = newer_data["meta"]["followed_user_ids"]
        if "followed_references" in newer_data["meta"].keys():
            exsited_data["meta"]["followed_references"][:0] = newer_data["meta"]["followed_references"]

        self.save_group_messages(exsited_data, group_id)
    ##############update()################################################


    def save_group_messages(self, dict_data, group_id):
        '''

        :param dict_data:
        :param group_id:
        :return: None
        '''

        file_name = 'group_%s_messages.json'%(group_id)
        file_path = os.path.join(DATA_PATH, file_name)

        print("DEBUG file_path: {}".format(file_path))
        with open(file_path, 'w') as fb:
            data_str = json.dumps(dict_data)
            fb.write(data_str)

        if group_id not in self.group_db.keys():
            self.group_db[group_id] = {"messages": None, "users": None}
        self.group_db[group_id]["messages"] = file_name

    ############save_group_messages()################################


    def save_group_users(self, dict_data, group_id):
        '''

        :param dict_data:
        :param group_id:
        :return: None
        '''

        file_name = 'group_%s_users.json'%(group_id)
        file_path = os.path.join(DATA_PATH, file_name)

        with open(file_path, 'w') as fb:
            data_str = json.dumps(dict_data)
            fb.write(data_str)

        self.group_db[group_id]["users"] = file_name

    ############save_group_users()################################


    def save_group_user_details(self, dict_data, group_id):
        '''
        Save each user detailed json file

        :param dict_data:
        :param group_id:
        :return:
        '''
        user_id = dict_data["id"]
        user_name = dict_data["full_name"]
        name_l = user_name.split(', ')
        user_name = name_l[0].upper() + '_' + name_l[1].split()[0]

        file_name = 'user_%s_%s.json'%(user_name, user_id)
        folder_name = 'group_%s'%(group_id)
        folder_path = os.path.join(DATA_PATH, folder_name)
        file_path = ''

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        else:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'w') as fb:
                data_str = json.dumps(dict_data)
                fb.write(data_str)
            print("user details is saved in {}".format(file_path))
    #################save_group_users_details()###################


    def get_group_messages(self, group_id):
        '''

        :param group_id:
        :return: dict
        format like: https://www.yammer.com/api/v1/messages/in_group/15273590.json
        '''

        file_name = 'group_%s_messages.json'%(group_id)
        file_path = os.path.join(DATA_PATH, file_name)

        if os.path.exists(file_path):
            with open(file_path, 'r') as fb:
                data_str = fb.read()
                dict_data = json.loads(data_str)
            return dict_data
        else:
            return None
    #############get_group_messages()########################


    def get_group_users(self, group_id):
        '''

        :param group_id:
        :return: dict
        format like: https://www.yammer.com/api/v1/users/in_group/15273590.json

        '''

        data_name = 'group_%s_users.json'%(group_id)
        data_path = os.path.join(DATA_PATH, data_name)

        if os.path.exists(data_path):
            with open(data_path, 'r') as fb:
                data_str = fb.read()
                dict_data = json.loads(data_str)
            return dict_data
        else:
            return None
    ################get_group_users()########################


    def get_user_info(self, user_id, group_id=None):
        '''
        Get one user's overall info from searching in the 'data' disk folder

        :param user_id:
        :param group_id:
        :return:
        '''

        if group_id == None:
            for group_id in self.group_db.keys():
                users_d = self.get_group_users(group_id)
                for user_d in users_d["users"]:
                    if user_id == user_d["id"]:
                        return user_d

        else:
            users_d = self.get_group_users(group_id)
            for user_d in users_d["users"]:
                if user_id == user_d["id"]:
                    return user_d

        return None
    #############get_user_info()#############################

    def  get_users_details(self, group_id):
        '''
        Find a user's detailed info from search in the specific gr

        :param user_id:
        :param group_id:
        :return: list containing user dict element
        '''
        dict_list = []
        if group_id == None:
            return

        folder_name = 'group_' + '%s'%(group_id)
        folder_path = os.path.join(DATA_PATH, folder_name)

        if os.path.exists(folder_path):
            for user_json in os.listdir(folder_path):
                if user_json.endswith('.json'):
                    with open(os.path.join(folder_path, user_json), 'r') as fb:
                        str_json = fb.read()
                        dict_json = json.loads(str_json)
                        dict_list.append(dict_json)

            return dict_list
        else:
            print("folder {} not found.".format(folder_path))
            return None
    ###########get_user_detailed_info()#####################




if __name__ == '__main__':
    my_db = My_Database()
    group_names = my_db.get_all_groups_name_id()
    print("DEBUG now we have group_names: {}".format(group_names))

    pass