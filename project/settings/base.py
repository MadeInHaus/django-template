import os.path
import sys

import djcelery

# Include apps on the path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

APPS_ROOT = os.path.join(PROJECT_ROOT, "apps")
if APPS_ROOT not in sys.path:
    sys.path.insert(0, APPS_ROOT)

WSGI_APPLICATION = "wsgi.application"

# People who get code error notifications when DEBUG=False
ADMINS = (('__PROJECT_SHORT_NAME__ administrator', '__ADMIN_EMAIL__'),)

DEFAULT_FROM_EMAIL = 'donotreply@madeinhaus.com'
SERVER_EMAIL = 'donotreply@madeinhaus.com'
EMAIL_SUBJECT_PREFIX = '[__PROJECT_SHORT_NAME__] '

# setting for using HTTPS or HTTP protocol for serving assets
USE_HTTPS_FOR_ASSETS = __USE_HTTPS_FOR_ASSETS__

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'vagrant',
        'PASSWORD': 'vagrant',
        'HOST': '',
        'PORT': '',
    }
}

SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2'
}


# Maximum size (in bytes) before an upload gets streamed to the file system.
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880

# List of locations of the fixture data files, in search order
FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'fixtures'),
)

# A tuple of strings designating all the enabled applications
INSTALLED_APPS = [
    'grappelli.dashboard',
    'grappelli',
    
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'django_extensions',

    'require',

    'gunicorn',
    'tastypie',
    'djcelery',
    'south',
    
    'utils',
    
]

# A tuple of IP addresses that see debug comments, when DEBUG is True
INTERNAL_IPS = ('0.0.0.0', '127.0.0.1',)

#Secure proxy setting 
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_SSL_PROXY', 'true')

# The language code for this installation
LANGUAGE_CODE = 'en-us'

# If login is successful, the view redirects to the URL specified in next.
# If next isn't provided, it redirects to settings.LOGIN_REDIRECT_URL
# (which defaults to /accounts/profile/).
LOGIN_REDIRECT_URL = '/admin'

# Who should get broken-link notifications when SEND_BROKEN_LINK_EMAILS=True
MANAGERS = ADMINS

# Absolute path to the directory that holds stored files.
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# URL that handles the media served from MEDIA_ROOT (must end in a slash)
MEDIA_URL = '/uploads/'

# A tuple of middleware classes to use
MIDDLEWARE_CLASSES = [
    # Site Optimization Middleware
    'utils.cache_headers_middleware.CacheHeadersMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',

    # Handle proxy redirects
    #'utils.set_domain_middleware.SetDomainMiddleware',
    #'utils.slash_redirect_middleware.SlashRedirectMiddleware',

    # Common Middleware
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Debug
    #'utils.profile_middleware.ProfileMiddleware',

    # Basic Auth
    #'utils.basic_auth_middleware.AuthMiddleware',

]


# CELERY SETTINGS
USE_CELERY = True
if USE_CELERY:
    # We use the database for the message store -- in apps that have more than one celery worker/lots of tasks we should use RabbitMQ or other high performance message queue
    BROKER_URL = 'django://'
    CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
    CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
    djcelery.setup_loader()

    # ADD celery apps 
    INSTALLED_APPS += [
                       'djcelery',
                       'kombu.transport.django',
                       ]

# REDIS SETTINGS
REDIS_HOST = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

# CACHING
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Never deploy a site into production with DEBUG turned on!
DEBUG = True

# Address to use for various automated correspondence from the site manager(s).
DEFAULT_FROM_EMAIL = 'hausheroku@gmail.com'

# Set the subject prefix for email messages sent to admins and managers
EMAIL_SUBJECT_PREFIX = '[Update Django Template]'

#DEFAULT_FROM_EMAIL = ''
#EMAIL_HOST = ''
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True




APPEND_SLASH = True

# Number of digits grouped together on the integer part of a number
NUMBER_GROUPING = 3

# The full Python import path to the root URLconf
ROOT_URLCONF = 'urls'

# Seed for secret-key hashing algorithms
SECRET_KEY = '__SECRET_KEY_SEED__'

# Whether files other than .html should be returned with the correct MIME type
SET_MIMETYPE = True

# The ID of the current site in the django_site database table
SITE_ID = 1


# Absolute path to the directory where collectstatic will collect static files
STATIC_ROOT = os.path.join(BASE_DIR, 'collected-static')

# URL to use when referring to static files located in STATIC_ROOT
STATIC_URL = '/static/'

# see django-require if S3 is required https://github.com/etianen/django-require
STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'

#should be off on production
SERVE_STATIC = False

# Additional locations the staticfiles app will traverse

DEV_STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_DIRS = (DEV_STATIC_ROOT,)

# The Site Title of your Admin-Interface. Change this instead of changing index.html
GRAPPELLI_ADMIN_TITLE = "__PROJECT_NAME__"
GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'


GRAPPELLI_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'

# Tastypie settings
TASTYPIE_DEFAULT_FORMATS = ['json', ]
TASTYPIE_API_LIMIT_PER_PAGE = 10000


# set cache times
APP_DEFAULT_CACHE = 10 #int(4 * 60 * 60)  # in seconds
APP_DEFAULT_SHORT_CACHE = 5 #int(15 * 60)  # in seconds
STATIC_DEFAULT_CACHE = 600 #int(365 * 24 * 60 * 60) # in seconds


# AWS settings
AWS_ACCESS_KEY_ID = os.environ.get('HAUS_AWS_ACCESS_KEY_ID','')
AWS_SECRET_ACCESS_KEY = os.environ.get('HAUS_AWS_SECRET_ACCESS_KEY','')

AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME = '__BUCKET_NAME__'
AWS_QUERYSTRING_AUTH = False


# AWS settings from https://github.com/etianen/django-herokuapp
AWS_AUTO_CREATE_BUCKET = False
AWS_HEADERS = {
    "Cache-Control": "public, max-age={}".format(STATIC_DEFAULT_CACHE),
}
AWS_S3_FILE_OVERWRITE = True
AWS_S3_SECURE_URLS = USE_HTTPS_FOR_ASSETS
AWS_S3_URL_PROTOCOL = '' # used to override protocol format, should be 'http:', 'https:' or ''
AWS_REDUCED_REDUNDANCY = False
AWS_IS_GZIPPED = True
AWS_PRELOAD_METADATA = True


TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'utils.context_processors.global_variables',

]

# Display a detailed report for any TemplateSyntaxError.
TEMPLATE_DEBUG = DEBUG

# List of locations of the template source files, in search order
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

# A tuple of template loader classes, specified as strings
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# The time zone for this installation
TIME_ZONE = None  #'America/Los_Angeles'

# Output the "Etag" header. This saves bandwidth but slows down performance
USE_ETAGS = False

# Enable Django's internationalization system
USE_I18N = False

# Display numbers and dates using the format of the current locale
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Testing
TEST_RUNNER = 'testing.TestRunner'

# Which settings are passed by RequestContext to the templates
# Keep this list small, as it is passed to each request.
# Uncomment more settings as needed
VIEW_SETTINGS = (
    'LANGUAGE_CODE',
    'TEMPLATE_DEBUG',
    'PERM_STATIC_URL'
)

LOG_FILENAME = None


# Django Require settings

# The baseUrl to pass to the r.js optimizer.
REQUIRE_BASE_URL = "js"

# The name of a build profile to use for your project, relative to REQUIRE_BASE_URL.
# A sensible value would be 'app.build.js'. Leave blank to use the built-in default build profile.
REQUIRE_BUILD_PROFILE = "app.build.js"

# The name of the require.js script used by your project, relative to REQUIRE_BASE_URL.
REQUIRE_JS = "libs/require.js"

# A dictionary of standalone modules to build with almond.js.
# See the section on Standalone Modules, below.
REQUIRE_STANDALONE_MODULES = {}

# Whether to run django-require in debug mode.
REQUIRE_DEBUG = False

# A tuple of files to exclude from the compilation result of r.js.
REQUIRE_EXCLUDE = ("build.txt",)

# The execution environment in which to run r.js: node or rhino.
REQUIRE_ENVIRONMENT = "node"

SHOW_TOOLBAR = False

if DEBUG and SHOW_TOOLBAR:
    print "showing toolbar..."
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + [
    
        # Debug
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'utils.profile_middleware.ProfileMiddleware',
    
    ]
    
    INSTALLED_APPS = INSTALLED_APPS + [
        'debug_toolbar',
    
    ]




# Debug toolbar settings
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_PATCH_SETTINGS = False

def custom_show_toolbar(request):
    return True  # Always show toolbar, for example purposes only.

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': 'project.settings.custom_show_toolbar',
    'EXTRA_SIGNALS': [],
    'HIDE_DJANGO_SQL': False,
    'INSERT_BEFORE': '</body>',
    'ENABLE_STACKTRACES' : True,
}

ALLOWED_HOSTS = ('localhost', )
