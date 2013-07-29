from settings import *
import dj_database_url
import sys

DEBUG = False

print >> sys.stderr, "Using Heroku Settings"


DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost'),
}

DATABASES['default']['ENGINE'] = 'django_postgrespool'


# this setting can be set to False after setting up a static file serve through a cdn
SERVE_STATIC = True

# AWS settings
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME = '__BUCKET_NAME__'

# suppress bucket auth via accesskeys
AWS_QUERYSTRING_AUTH = False

STATICFILES_STORAGE = 'utils.storage.OptimizedS3BotoStorage'
DEFAULT_FILE_STORAGE = "utils.storage.MediaRootS3BotoStorage"

STATIC_URL = 'https://s3.amazonaws.com/{}/'.format(AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = 'https://s3.amazonaws.com/{}/uploads/'.format(AWS_STORAGE_BUCKET_NAME)

INSTALLED_APPS += ('storages',)
