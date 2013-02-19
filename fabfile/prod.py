from fabric.api import task, local, run, cd, abort
from fabric.context_managers import shell_env

from vagrant import collectstatic, css_compile, killall
from fabric.decorators import roles
from fabric.contrib import django
import os

import logging
logging.basicConfig()
log = logging.getLogger(__name__)

PROD_ENV = "heroku"

def parse_vars(string):
    d = {}
    for line in string.split('\n'):
        if '=' not in line:
            continue
        name, value = line.strip().split('=')
        value = value.strip('"')
        d[name] = value
    return d

@task
@roles('vagrant')
def compile_prod_css():
    log.warning('Calling killall,  all process will be killed!')
    killall()
    
    with  shell_env(APP_ENV=PROD_ENV):
        with cd("/var/www"):
            settings = parse_vars(run("./manage.py settings_vars STATIC_URL"))
            if 'STATIC_URL' not in settings:
                log.error('STATIC_URL lookup failed!!!')
                abort("STATIC_URL lookup failed!!!") 
        
    with shell_env(APP_ENV=PROD_ENV, STATIC_URL=settings['STATIC_URL']):
        css_compile()
    
    log.warning('Note killall was called so vagrant server/compass will be down')


@task
@roles('vagrant')
def deploy():
    local('git push production master:master')
    compile_prod_css()
    deploy_static_media()
    deploy_user_media()

@task
@roles('vagrant')
def deploy_static_media():
    with shell_env(APP_ENV=PROD_ENV):
        collectstatic(no_input=True)
    
@task
@roles('vagrant')
def deploy_user_media():
    with  shell_env(APP_ENV=PROD_ENV):
        with cd("/var/www"):
            run('./manage.py sync_media_s3 --prefix=uploads')

@task
@roles('vagrant')
def sync_prod_db(reset_db=False):
    if reset_db:
        # uncomment below and replace DATABSE_URL with the prod database url
        # note that this is destructive of the PROD DB
        #local('heroku pg:reset DATABASE_URL') #add "--confirm haus" to remove required input
        pass
    local('heroku run ./manage.py syncdb')
    local('heroku run ./manage.py migrate')
    