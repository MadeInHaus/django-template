from fabric.api import local, cd, get, env, roles, execute, task, run, settings

@task
@roles('vagrant')
def runserver():
	with settings(warn_only=True):
		# FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
		run("ps ax | grep [r]unserver | awk '{ print $1 }' | xargs kill -9")
	with cd("/var/www/project"):
		run('python ./manage.py runserver [::]:8000')

@task
@roles('vagrant')
def gunicorn():
	with settings(warn_only=True):
		# FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
		run("ps ax | grep [r]un_gunicorn | awk '{ print $1 }' | xargs kill -9")
	with cd("/var/www/project"):
		run('python ./manage.py run_gunicorn [::]:8000')

@task
@roles('vagrant')
def celery():
	with settings(warn_only=True):
		# FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
		run("ps ax | grep [w]orker | awk '{ print $1 }' | xargs kill -9")
	with cd("/var/www/project"):
		run('python manage.py celery worker --loglevel=INFO')


@task
@roles('vagrant')
def celerybeat():
	with settings(warn_only=True):
		# FOR SOME REASON IF THE PROCESS WASN'T ENDED CORRECTLY, THIS WILL KILL IT
		run("ps ax | grep [c]elerybeat | awk '{ print $1 }' | xargs kill -9")
	with cd("/var/www/project"):
		run('python manage.py celerybeat --loglevel=INFO')

@task
@roles('vagrant')		
def syncdb():
    with cd("/var/www/project"):
        run('python ./manage.py syncdb')