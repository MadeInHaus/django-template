from settings import *
import dj_database_url
import sys

import os

from json import load

DEBUG = False

print >> sys.stderr, "Using Heroku Settings"

try:
    APP_INFO = load(open(BASE_DIR + "/app_info.json"))['production']
except:
    print "Failed to load app_info.json"
    APP_INFO = {}

print "using appinfo: ", APP_INFO

if APP_INFO.get('project_name') and APP_INFO.get('branch_name'):
    STATIC_PREPEND_PATH = '/{}/{}'.format(APP_INFO.get('project_name'), APP_INFO.get('branch_name'))
else:
    STATIC_PREPEND_PATH = ''


DATABASES = {
    'default': dj_database_url.config(default='postgres://localhost'),
}


# this setting can be set to False after setting up a static file serve through a cdn
SERVE_STATIC = True

# AWS settings
AWS_ACCESS_KEY_ID = os.environ.get('HAUS_AWS_ACCESS_KEY_ID','')
AWS_SECRET_ACCESS_KEY = os.environ.get('HAUS_AWS_SECRET_ACCESS_KEY','')

AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME = '__BUCKET_NAME__'

# suppress bucket auth via accesskeys
AWS_QUERYSTRING_AUTH = False

ASSET_PROTOCOL = 'https' if USE_HTTPS_FOR_ASSETS else 'http'

USE_RELATIVE_STATIC_URL = os.environ.get('USE_RELATIVE_STATIC_URL', False)

if USE_RELATIVE_STATIC_URL:
    STATIC_URL = '/'
    MEDIA_URL = '/uploads/'
else:
    STATIC_URL = '{}://s3.amazonaws.com/{}/'.format(ASSET_PROTOCOL, AWS_STORAGE_BUCKET_NAME)
    MEDIA_URL = '{}://s3.amazonaws.com/{}/uploads/'.format(ASSET_PROTOCOL, AWS_STORAGE_BUCKET_NAME)

    STATICFILES_STORAGE = 'utils.storage.OptimizedS3BotoStorage'
    DEFAULT_FILE_STORAGE = "utils.storage.MediaRootS3BotoStorage"

    INSTALLED_APPS += ('storages',)

ALLOWED_HOSTS += ('{}.herokuapp.com'.format(APP_INFO.get('heroku_app_name','')), )