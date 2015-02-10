from os import path
from fabric.api import local, cd, lcd, roles, execute, task, run, \
                       settings, abort, hide
from fabric.colors import yellow


from haus_vars import with_vars


import logging
logging.basicConfig()
log = logging.getLogger(__name__)

# config....
use_celery = False # this should match the USE_CELERY setting in project.settings
# paths
base_path   = "./project/static"
css_path    = base_path + "/css/"
config_path = css_path + "config.rb"


# sass execs
exec_sass_watch   = "compass watch --poll {} -c {}"
exec_sass_compile = "compass compile {} -c {} --trace --force"



@task
@roles('vagrant')
def test_vagrant():
    local_md5 = local('md5 README.md', capture=True).split()[3]
    with cd('/var/www'):
        remote_md5 = run('md5sum README.md').split()[0]
    if not local_md5 == remote_md5:
        abort('VM does not match,  another VM running? got local: {} and remote: {}'.format(local_md5, remote_md5))


@task
@roles('vagrant')
@with_vars
def env_test(*args, **kwargs):
    print 'args: {} kwargs: {}'.format(args, kwargs)
    run('env | grep HAUS')

@task
def runall():
    execute(test_vagrant)
    local('touch nohup.out')
    if use_celery:
        local('nohup fab vagrant.celery &')
        local('nohup fab vagrant.celerybeat &')
    local('fab vagrant.css_watch_halt')
    local('nohup fab vagrant.css_watch_ &')
    local('nohup fab vagrant.runserver &')
    local('tail -f nohup.out')

@task
@roles('vagrant')
def killall():
    execute(test_vagrant)
    log.warning(yellow('killing all processes'))
    with settings(warn_only=True):
        with hide('warnings', 'running', 'stderr', 'stdout'):
            run("ps ax | grep [r]unserver | awk '{ print $1 }' | xargs sudo kill -9")
            run("ps ax | grep [r]un_gunicorn | awk '{ print $1 }' | xargs sudo kill -9")
            if use_celery:
                run("ps ax | grep [w]orker | awk '{ print $1 }' | xargs sudo kill -9")
                run("ps ax | grep [c]elerybeat | awk '{ print $1 }' | xargs sudo kill -9")
            run("ps ax | grep [c]ompass | awk '{ print $1 }' | xargs sudo kill -9")
            run("ps ax | grep [s]ass | awk '{ print $1 }' | xargs sudo kill -9")

@task
@roles('vagrant')
def runserver():
    with settings(warn_only=True):
        with hide('warnings', 'running', 'stderr', 'stdout'):
            # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
            run("ps ax | grep [r]unserver | awk '{ print $1 }' | xargs kill -9")
    with cd("/var/www"):
        run('python ./manage.py runserver [::]:8000')

@task
@roles('vagrant')
def gunicorn():
    with settings(warn_only=True):
        with hide('warnings', 'running', 'stderr', 'stdout'):
            # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
            run("ps ax | grep [r]un_gunicorn | awk '{ print $1 }' | xargs kill -9")
    with cd("/var/www"):
        run('gunicorn project.wsgi::application [::]:8000')

@task
@roles('vagrant')
def celery():
    with settings(warn_only=True):
        with hide('warnings', 'running', 'stderr', 'stdout'):
            # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
            run("ps ax | grep [w]orker | awk '{ print $1 }' | xargs kill -9")
    with cd("/var/www"):
        run('python manage.py celery worker --loglevel=DEBUG')


@task
@roles('vagrant')
def celerybeat():
    with settings(warn_only=True):
        with hide('warnings', 'running', 'stderr', 'stdout'):
            # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
            run("ps ax | grep [c]elerybeat | awk '{ print $1 }' | xargs kill -9")
    with cd("/var/www"):
        run('python manage.py celerybeat --loglevel=INFO')

@task
@roles('vagrant')
def initdb(load_images=False):
    with cd("/var/www"):
        run('yes no | python manage.py syncdb')
        run('python manage.py migrate')
        run('python manage.py createadmin')

    if load_images:
        load_fixture_images()
    load_fixtures()


@task
@roles('vagrant')
def syncdb():
    with cd("/var/www"):
        run('python manage.py migrate')

@task
@roles('vagrant')
def resetall():
    """Stop all services, destroy the database, restore it from fixtures, remove all files in uploads directory and download assets."""
    killall()
    local('vagrant provision')
    resetdb(delete_images=True, load_images=True)

@task
@roles('vagrant')
def resetdb(load_images=False, delete_images=False):
    # mysql
    #run("mysql -u vagrant -pvagrant -e 'drop database if exists django'")
    #run('mysql -u vagrant -pvagrant -e "create database django"')
    killall()

    # postgres
    run('dropdb django')
    run('createdb django')

    if delete_images:
        run("mkdir -p /var/www/uploads")
        with cd("/var/www/uploads"):
            run('rm -rf ./*')

    initdb(load_images)

@task
def load_fixtures():
    with cd("/var/www"):
        run("python manage.py loaddata  project/fixtures/local_data.json")


@task
def load_fixture_images():
    # basic media fixture stub
    uploads_dir = path.abspath(path.join(path.dirname(__file__), '../uploads'))
    with lcd(uploads_dir):
        with settings(warn_only=True):
            local('rm -rf ./*')
        #local('curl -sLO https://domain/assets.tar.bz2')
        #local('tar xjvf assets.tar.bz2')
        #local('rm assets.tar.bz2')

@task
@roles('vagrant')
def collectstatic(no_input=False, skip_admin=False):
    with cd("/var/www"):
        run('python manage.py collectstatic {} {}'.format('--noinput' if no_input else '', '-i "admin*" -i "grappelli*"' if skip_admin else ''))

@task
@roles('vagrant')
def css_watch():
    with settings(warn_only=True):
        with hide('warnings', 'running', 'stderr', 'stdout'):
            # Killing all sass processes before executing a new one
            run("ps ax | grep [c]ompass | awk '{ print $1 }' | xargs sudo kill -9")

    with cd("/var/www"):
        run(exec_sass_watch.format(base_path, config_path))

@task
@roles('vagrant')
def pipinstall():
    run('/home/vagrant/.venv/bin/pip install --use-mirrors -r /var/www/requirements.txt')

@task
@roles('vagrant')
def freeze():
    run('/home/vagrant/.venv/bin/pip freeze > /var/www/current-requirements.txt')

@task
@roles('vagrant')
def css_compile():
    with cd("/var/www"):
        run(exec_sass_compile.format(base_path, config_path))

@task
@roles('vagrant')
def test():
    with cd("/var/www"):
        run('python manage.py test')

