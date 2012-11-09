# Customize this script if need to launch a configurable conf file. EI: -c `hostname`.py

exec /srv/active/env/bin/gunicorn_django -c /srv/active/deploy/gunicorn/gunicorn.py /srv/active/project/settings/__init__.py
