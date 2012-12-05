from settings import *
import dj_database_url

DEBUG = False

print "Using Heroku Settings"


DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost'),
}

