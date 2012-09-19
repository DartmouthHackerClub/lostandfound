#!/usr/bin/env python
from fabric.api import *

def test():
    env.hosts = ['staging.hacktown.cs.dartmouth.edu']
    env.user = 'deploy'

def prod():
    env.hosts = ['flask.hacktown.cs.dartmouth.edu']
    env.user = 'zach'

def update():
    with cd('/srv/http/flask/env/flask_template'):
        run('git pull')
        with prefix('source ../bin/activate'):
            run('pip install -r requirements.txt')

def restart():
    sudo('supervisorctl restart flask')

def deploy():
    update()
    restart()
