import os
pythonpath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../project/'))
bind = "127.0.0.1:8000"

# Make sure to tune
workers = 10

loglevel = "WARNING"
logfile = "/var/log/gunicorn/errors.log"
django_settings = "settings"
