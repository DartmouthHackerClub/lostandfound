#!/usr/bin/env python
from fabric.api import *

def test():
    env.hosts = ['staging.hacktown.cs.dartmouth.edu']
    env.user = 'deploy'

def prod():
    env.hosts = ['production.hacktown.cs.dartmouth.edu']
    env.user = 'deploy'

def update():
    with cd('/home/deploy/env/app_name/app_name'):
        run('git pull')
        with prefix('source ../bin/activate'):
            run('pip install -r requirements.txt')

def restart():
    sudo('supervisorctl restart app_name')

def deploy():
    update()
    restart()
