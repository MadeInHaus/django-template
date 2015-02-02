web: newrelic-admin run-program gunicorn project.wsgi:application -b 0.0.0.0:$PORT -k gevent -w 5
celeryd: newrelic-admin run-program python manage.py celeryd -E -B --loglevel=INFO
