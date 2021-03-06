from fabric.api import local, run, cd, lcd, task
from fabric.tasks import Task
from fabric.context_managers import settings

from vagrant import collectstatic, killall
from fabric.colors import red, green, yellow

from haus_vars import with_vars, APP_INFO

from os import path

import logging
import urllib2
import json
import subprocess

logging.basicConfig()
log = logging.getLogger(__name__)

# suppress tasks
__all__ = []




def get_hash(env):
    print red("CHECKING OUT BRANCH: {}".format(APP_INFO[env]["branch_name"]))
    local('git checkout {}'.format(APP_INFO[env]["branch_name"]))
    return local('git rev-parse HEAD', capture=True).strip()[:20]

def get_heroku_asset_version(env):
    git_hash = local('heroku config:get ASSET_VERSION -a {}'.format(APP_INFO[env]["heroku_app_name"]), capture=True)
    print "got hash: ", yellow('{}'.format(git_hash))
    return git_hash


def set_heroku_asset_version(env, git_hash):
    local('heroku config:set ASSET_VERSION={} -a {}'.format(git_hash, APP_INFO[env]["heroku_app_name"]))

def set_heroku_maintenance_page(env, url):
    local('heroku config:set MAINTENANCE_PAGE_URL={} -a {}'.format(url, APP_INFO[env]["heroku_app_name"]))

def set_heroku_error_page(env, url):
    local('heroku config:set ERROR_PAGE_URL={} -a {}'.format(url, APP_INFO[env]["heroku_app_name"]))


def current_asset_version(env, ):
    return get_hash(env)



class CustomTask(Task):
    '''Creates a task from a task with the ability to set default arguments and env var'''
    roles = ['vagrant']
    
    def __init__(self, func, env, *args, **kwargs):
        super(CustomTask, self).__init__(*args, **kwargs)
        self.func = func
        self.env = env
        self.name = func.__name__
        self.__doc__ = func.__doc__
        self.default_args = kwargs

    def run(self, *args, **kwargs):
        kwargs.update(self.default_args)
        if 'env' not in kwargs:
            kwargs['env'] = self.env
        return self.func(*args, **kwargs)



def deploy(env=None, quick=True):
    # ensure quick=='False' is properly handled
    if str(quick).lower() == 'false':
        quick = False

    """Deploy static and source to heroku environment"""
    notify_slack(env=env)
    version = get_heroku_asset_version(env) if quick else current_asset_version(env=env)
    deploy_static_media(env=env, asset_version=version, quick=quick)
    deploy_maintenance_pages(env=env, asset_version=version, quick=quick)
    deploy_source(env=env, asset_version=version, quick=quick)

@with_vars
def deploy_maintenance_pages(env=None, asset_version='', quick=False, haus_vars={}):
    url = "{}error.html".format(haus_vars['STATIC_URL'])
    set_heroku_error_page(env, url)
    set_heroku_maintenance_page(env, url)

@with_vars
def deploy_source(env=None, asset_version='', quick=False, haus_vars={}):
    """Deploy source to heroku environment"""
    print green('Deploying source to Heroku')
    local('git push {} {}:master'.format(APP_INFO[env]["heroku_remote_name"], APP_INFO[env]["branch_name"]))
    sync_prod_db(env=env)
    if not quick:
        set_heroku_asset_version(env, asset_version)


@with_vars
def deploy_static_media(env=None, asset_version='', quick=False, haus_vars={}):
    """Deploy static (runs collectstatic within given environment)"""
    print green('Deploying static media {}'.format('__quick__' if quick else ''))
    collectstatic(no_input=True, skip_admin=quick)


@with_vars
def deploy_user_media(env=None, haus_vars={} ):
    """Deploy user media to media location on s3"""
    print green('Deploying user media')
    with cd("/var/www"):
        run('./manage.py sync_media_s3 --prefix=uploads')


@with_vars
def sync_prod_db(env=None, reset_db=False, haus_vars={}):
    """Run syncdb and migrate within given environment"""
    print green('sync/migrate DB')
    if reset_db:
        # uncomment below and replace DATABSE_URL with the prod database url
        # note that this is destructive of the PROD DB
        #local('heroku pg:reset DATABASE_URL') #add "--confirm haus" to remove required input
        pass
    local('heroku run ./manage.py migrate -a {}'.format(APP_INFO[env]["heroku_app_name"]))


# Project setup

@task
def remotes():
    """setup the heroku git remotes per the app_info.json config file"""
    # heroku env remotes
    for env in ('dev', 'staging', 'production'):
        app_name = APP_INFO[env]['heroku_app_name']
        if not app_name.startswith('app-name'):
            with settings(warn_only=True): 
                local("git remote add {} git@heroku.com:{}.git".format(APP_INFO[env]['heroku_remote_name'], app_name))


# Fixture Production
# ------------------

@with_vars
def create_fixture_on_s3(env=None, haus_vars={}):
    local('heroku run ./manage.py create_upload_fixture -a {}'.format(APP_INFO[env]["heroku_app_name"]))


@with_vars
def grab_fixture_on_s3(env=None, haus_vars={}):
    fixture_dir = path.abspath(path.join(path.dirname(__file__), '../project/fixtures/'))
    fixture_url = '{}fixtures/local_data.json'.format(haus_vars['STATIC_URL'])
    with lcd(fixture_dir):
        local('curl --output local_data.json {}'.format(fixture_url))
        print 'downloaded: {} to: {}'.format(fixture_url, fixture_dir)


@with_vars
def apply_fixture(env=None, haus_vars={}):
    local('heroku run ./manage.py loaddata project/fixtures/local_data.json -a {}'.format(APP_INFO[env]["heroku_app_name"]))


# Notify Slack
# ------------------

@with_vars
def notify_slack(env=None, haus_vars={}):
    slack_webhook_token =  APP_INFO[env].get("slack_webhook_token")
    if slack_webhook_token:
        slack_url = "https://haus.slack.com/services/hooks/incoming-webhook?token={}".format(slack_webhook_token)
        try:
            name = subprocess.check_output(['git', 'config', 'user.name']).strip()
        except:
            name = 'unknown'
        slack_message = "credits rolling on: {} as requested by {} :crocodile:".format(APP_INFO[env]["heroku_app_name"], name)
        payload={
            "username": "deployerbot",
            "text": slack_message
        }
        req = urllib2.Request(slack_url, json.dumps(payload))
        urllib2.urlopen(req)


