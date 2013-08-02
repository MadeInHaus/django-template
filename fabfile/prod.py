from fabric.api import task, local, run, cd, abort
from fabric.context_managers import shell_env

from vagrant import collectstatic, css_compile, killall
from fabric.decorators import roles
from fabric.contrib import django
from fabric.colors import red, green, yellow
import os

import logging
from json import load
logging.basicConfig()
log = logging.getLogger(__name__)


try:
    APP_INFO = load(open("app_info.json"))['prod']
except:
    print red("Failed to load app_info.json")
    abort()

print "using appinfo: ", green(APP_INFO)

APP_ENV_NAME = APP_INFO["app_env_name"]
HEROKU_APP_NAME = APP_INFO["heroku_app_name"]
HEROKU_REMOTE_NAME = APP_INFO["heroku_remote_name"]



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
def compile_css():
    log.warning(red('Calling killall,  all process will be killed!'))
    killall()

    with  shell_env(APP_ENV=APP_ENV_NAME):
        with cd("/var/www"):
            settings = parse_vars(run("./manage.py settings_vars STATIC_URL"))
            if 'STATIC_URL' not in settings:
                log.error('STATIC_URL lookup failed!!!')
                abort("STATIC_URL lookup failed!!!") 

    with shell_env(APP_ENV=APP_ENV_NAME, STATIC_URL=settings['STATIC_URL']):
        css_compile()

    log.warning(red('Note killall was called so vagrant server/compass will be down'))

def get_hash():
    return local('git rev-parse HEAD', capture=True).strip()[:20]


@task
@roles('vagrant')
def get_heroku_asset_version():
    hash = local('heroku config:get ASSET_VERSION', capture=True)
    print "got hash: ", yellow('{}'.format(hash))
    return hash


@task
@roles('vagrant')
def set_heroku_asset_version(hash):
    local('heroku config:set ASSET_VERSION={} -a {}'.format(hash, HEROKU_APP_NAME))
    pass


@task
@roles('vagrant')
def current_asset_version():
    return get_hash()
#     print red('hash: {}'.format(get_hash()))



@task
@roles('vagrant')
def deploy():
    compile_css()
    version = current_asset_version()
    deploy_static_media(ASSET_VERSION=version)
    local('git push production master:master')
    sync_prod_db()
    set_heroku_asset_version(version)


@task
@roles('vagrant')
def deploy_static_media(ASSET_VERSION=''):
    with shell_env(APP_ENV=APP_ENV_NAME, ASSET_VERSION=ASSET_VERSION):
        collectstatic(no_input=True)


@task
@roles('vagrant')
def deploy_user_media():
    with  shell_env(APP_ENV=APP_ENV_NAME):
        with cd("/var/www"):
            run('./manage.py sync_media_s3 --prefix=uploads')


@task
@roles('vagrant')
def sync_prod_db(reset_db=False):
    print green('sync/migrate DB')
    if reset_db:
        # uncomment below and replace DATABSE_URL with the prod database url
        # note that this is destructive of the PROD DB
        #local('heroku pg:reset DATABASE_URL') #add "--confirm haus" to remove required input
        pass
    local('heroku run ./manage.py syncdb')
    local('heroku run ./manage.py migrate')
    