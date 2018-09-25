#!/usr/bin/env python3

import os

#ACCESS_TOKEN = '592-sGkKVOjrGBIUMF6jfiphhQ'
try:
    ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
except KeyError:
    ACCESS_TOKEN = None



print("DEBUG my_constants.py, ACCESS_TOKEN: {}".format(ACCESS_TOKEN))



