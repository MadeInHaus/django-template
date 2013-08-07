from fabric.api import local, run, cd, abort
from fabric.tasks import Task
from fabric.context_managers import shell_env

from vagrant import collectstatic, css_compile, killall
from fabric.colors import red, green, yellow

import logging
from json import load
logging.basicConfig()
log = logging.getLogger(__name__)

# suppress tasks
__all__ = []

try:
    APP_INFO = load(open("app_info.json"))
except:
    print red("Failed to load app_info.json")
    abort()

#print "using appinfo: ", green(app_INFO)


def parse_vars(string):
    d = {}
    for line in string.split('\n'):
        if '=' not in line:
            continue
        name, value = line.strip().split('=')
        value = value.strip('"')
        d[name] = value
    return d


def compile_env_css(env, ):
    log.warning(red('Calling killall,  all process will be killed!'))
    killall()

    with  shell_env(app_env=APP_INFO[env]["app_env_name"]):
        with cd("/var/www"):
            settings = parse_vars(run("./manage.py settings_vars STATIC_URL"))
            if 'STATIC_URL' not in settings:
                log.error('STATIC_URL lookup failed!!!')
                abort("STATIC_URL lookup failed!!!") 

    with shell_env(app_env=APP_INFO[env]["app_env_name"], STATIC_URL=settings['STATIC_URL']):
        css_compile()

    log.warning(red('Note killall was called so vagrant server/compass will be down'))


def get_hash(env, ):
    print red("CHECKING OUT BRANCH: {}".format(APP_INFO[env]["branch_name"]))
    local('git checkout {}'.format(APP_INFO[env]["branch_name"]))
    return local('git rev-parse HEAD', capture=True).strip()[:20]


def get_heroku_asset_version(env, ):
    git_hash = local('heroku config:get ASSET_VERSION -a {}'.format(APP_INFO[env]["heroku_app_name"]), capture=True)
    print "got hash: ", yellow('{}'.format(git_hash))
    return git_hash


def set_heroku_asset_version(env, git_hash):
    local('heroku config:set ASSET_VERSION={} -a {}'.format(git_hash, APP_INFO[env]["heroku_app_name"]))


def current_asset_version(env, ):
    return get_hash(env)




class CustomTask(Task):
    roles = ['vagrant']
    
    def __init__(self, func, myarg, *args, **kwargs):
        super(CustomTask, self).__init__(*args, **kwargs)
        self.func = func
        self.myarg = myarg
        self.name = func.__name__
        self.__doc__ = func.__doc__

    def run(self, *args, **kwargs):
        return self.func(self.myarg, *args, **kwargs)




def deploy(env, ):
    """Deploy static and source to heroku environment"""
    compile_env_css(env)
    version = current_asset_version(env)
    deploy_static_media(env, asset_version=version)
    deploy_source(env, asset_version=version)


def deploy_source(env, asset_version=''):
    """Deploy source to heroku environment"""
    local('git push {} {}:master'.format(APP_INFO[env]["heroku_remote_name"], APP_INFO[env]["branch_name"]))
    sync_prod_db(env)
    set_heroku_asset_version(env, asset_version)


def deploy_static_media(env, asset_version=''):
    """Deploy static (runs collectstatic within given environment)"""
    with shell_env(app_env=APP_INFO[env]["app_env_name"], asset_version=asset_version):
        collectstatic(no_input=True)


def deploy_user_media(env, ):
    """Deploy user media to media location on s3"""
    with  shell_env(app_env=APP_INFO[env]["app_env_name"]):
        with cd("/var/www"):
            run('./manage.py sync_media_s3 --prefix=uploads')


def sync_prod_db(env, reset_db=False):
    """Run syncdb and migrate within given environment"""
    print green('sync/migrate DB')
    if reset_db:
        # uncomment below and replace DATABSE_URL with the prod database url
        # note that this is destructive of the PROD DB
        #local('heroku pg:reset DATABASE_URL') #add "--confirm haus" to remove required input
        pass
    local('heroku run ./manage.py syncdb -a {}'.format(APP_INFO[env]["heroku_app_name"]))
    local('heroku run ./manage.py migrate -a {}'.format(APP_INFO[env]["heroku_app_name"]))

