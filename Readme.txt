Python3 use yampy2 which is an update of the official yampy(yampy3 for python3):
install: pip install yampy3

There is another updated yampy:
github: https://github.com/tonybaloney/yampy2
web: https://yampy2.readthedocs.io/en/latest/quickstart.html


Heroku git remote:
heroku git:remote -a yammerstate
https://git.heroku.com/yammerstate.git

heroku ps
heroku ps:scale worker=1

����heroku�Ļ�������(win�£�

heroku config:set SECRET_KEY='hard to guess'

�鿴��������
heroku config

�������ݿ�:
heroku addons:create heroku-postgresql:hobby-dev --app yammerstate


Oauth:
auth_url = 'https://www.yammer.com/dialog/oauth?client_id=2fxbPxiDYwtM40yN3m0fQ&redirect_uri=https%3A%2F%2Fyammerstate.herokuapp.com'