#!/usr/bin/env python3

import os
from dotenv import load_dotenv
load_dotenv()

#ACCESS_TOKEN = '592-sGkKVOjrGBIUMF6jfiphhQ'
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
print("DEBUG my_constants.py, ACCESS_TOKEN: {}".format(ACCESS_TOKEN))
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")
AUTH_URL = "https://www.yammer.com/oauth2/authorize?client_id=" \
           + CLIENT_ID + "&response_type=code&redirect_uri=" + REDIRECT_URL



