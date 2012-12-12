from subprocess import Popen
from fabric.api import local, cd, get, env, roles, execute, task, run, settings
from fabric.colors import yellow


# paths
base_path           = "./project/static/css"
src_path   = base_path + "/src"
css_path    = base_path + "/"

# sass execs
exec_sass_watch   = "sass -l --watch {}:{}"
exec_sass_compile = "sass --update --style compressed {}:{}"


@task
def runall():
    local('nohup fab vagrant.celery &')
    local('nohup fab vagrant.celerybeat &')
    local('nohup fab vagrant.css_watch &')
    local('nohup fab vagrant.runserver &')
    local('tail -f nohup.out')

@task
@roles('vagrant')
def killall():
    with settings(warn_only=True):
        run("ps ax | grep [r]unserver | awk '{ print $1 }' | xargs sudo kill -9")
        run("ps ax | grep [r]un_gunicorn | awk '{ print $1 }' | xargs sudo kill -9")
        run("ps ax | grep [w]orker | awk '{ print $1 }' | xargs sudo kill -9")
        run("ps ax | grep [c]elerybeat | awk '{ print $1 }' | xargs sudo kill -9")
        run("ps ax | grep [s]ass | awk '{ print $1 }' | xargs sudo kill -9")

@task
@roles('vagrant')
def runserver():
    with settings(warn_only=True):
        # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
        run("ps ax | grep [r]unserver | awk '{ print $1 }' | xargs kill -9")
    with cd("/var/www"):
        run('python ./manage.py runserver [::]:8000')

@task
@roles('vagrant')
def gunicorn():
    with settings(warn_only=True):
        # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
        run("ps ax | grep [r]un_gunicorn | awk '{ print $1 }' | xargs kill -9")
    with cd("/var/www"):
        run('python ./manage.py run_gunicorn [::]:8000')

@task
@roles('vagrant')
def celery():
    with settings(warn_only=True):
        # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
        run("ps ax | grep [w]orker | awk '{ print $1 }' | xargs kill -9")
    with cd("/var/www"):
        run('python manage.py celery worker --loglevel=INFO')


@task
@roles('vagrant')
def celerybeat():
    with settings(warn_only=True):
        # FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
        run("ps ax | grep [c]elerybeat | awk '{ print $1 }' | xargs kill -9")
    with cd("/var/www"):
        run('python manage.py celerybeat --loglevel=INFO')

@task
@roles('vagrant')        
def initdb():
    with cd("/var/www"):
        run('yes no | python manage.py syncdb')
        run('python manage.py migrate')
        run('python manage.py createsuperuser --username=user --email=user@host.com')


@task
@roles('vagrant')        
def syncdb():
    with cd("/var/www"):
        run('python manage.py syncdb')
        run('python manage.py migrate')

@task
@roles('vagrant')        
def resetdb():
    # mysql
    #run("mysql -u vagrant -pvagrant -e 'drop database if exists django'")
    #run('mysql -u vagrant -pvagrant -e "create database django"')
    
    # postgres
    run('dropdb django')
    run('createdb django')
    initdb()


@task
@roles('vagrant')
def collectstatic():
    with cd("/var/www"):
        run('python manage.py collectstatic')

@task
@roles('vagrant')
def css_watch():
    with cd("/var/www"):
        run(exec_sass_watch.format(src_path, css_path))

@task
def css_compile():
    with cd("/var/www"):
        run(exec_sass_compile.format(src_path, css_path))