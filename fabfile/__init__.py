from fabric.api import local, cd, get, env, roles, execute, task, run

env.roledefs       = {
                      'vagrant'                : ['vagrant@127.0.0.1:2222']
                     }
env.passwords      = {
                      'vagrant@127.0.0.1:2222'      :'vagrant',
                     }

@task
@roles('vagrant')
def runserver():
	run("ps ax | grep [p]ython | awk '{ print $1 }' | xargs kill -9")
	with cd("/var/www/project"):
		run('python ./manage.py runserver [::]:8000')

@task
@roles('vagrant')		
def syncdb():
    with cd("/var/www/project"):
        run('python ./manage.py syncdb')