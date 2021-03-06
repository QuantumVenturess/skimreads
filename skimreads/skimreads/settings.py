# Django settings for skimreads project.
import os, socket

# Check environment
if os.environ.get('MYSITE_PRODUCTION', False):
    # production
    DEBUG = TEMPLATE_DEBUG = True
    DEV = False
    COMPRESS_ENABLED = True
else:
    # development
    DEBUG = TEMPLATE_DEBUG = True
    DEV = True
    COMPRESS_ENABLED = False

# Project name
project_name = 'skimreads'

# Admins
ADMINS = (
    ('Tommy Dang', 'tommydangerouss@gmail.com')
)

# Authentication
AUTH_PROFILE_MODULE = 'skimreads.Profile'

AUTHENTICATION_BACKENDS = (
    'skimreads.backends.EmailAuthBackend',
    'skimreads.backends.FacebookAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Amazon S3
AWS_ACCESS_KEY_ID       = os.environ.get('AMAZON_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY   = os.environ.get('AMAZON_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = project_name
if DEV:
    BUCKET_NAME = project_name + '_development'
else:
    BUCKET_NAME = project_name

AWS_HEADERS = {
    'Expires': 'Sun, 19 Jul 2020 18:06:32 GMT'
}

AWS_QUERYSTRING_AUTH = False

# Database
if DEV:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.postgresql_psycopg2',
            'NAME':     'skimreads',
            'USER':     'postgres',
            'PASSWORD': 'postgres',
            'HOST':     '',
            'PORT':     '5432',
        }
    }
else:
    # Parse database configuration from $DATABASE_URL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=os.environ['DATABASE_URL'])
    }

# Email
EMAIL_HOST =          'smtp.gmail.com' # The host to use for sending email
EMAIL_HOST_USER =     'quantumventuress@gmail.com' # Username to use for the SMTP server
EMAIL_HOST_PASSWORD = '' # Password for username
EMAIL_PORT =          587 # Port to use for the SMTP server defined in EMAIL_HOST
EMAIL_USE_TLS =       True
DEFAULT_FROM_EMAIL =  '' # Default email address to use for various automated correspondence
SERVER_EMAIL =        '' # The email address that error messages come from

# Facebook
if DEV:
    FACEBOOK_APP_ID = '347204595370545'
    FACEBOOK_APP_SECRET = 'a90e8d7ee81d99b4741918c3e911e5ad'
    FACEBOOK_REDIRECT_URI = 'http://localhost:8000/oauth/facebook/authenticate'
else:
    FACEBOOK_APP_ID       = os.environ.get('FACEBOOK_APP_ID')
    FACEBOOK_APP_SECRET   = os.environ.get('FACEBOOK_APP_SECRET')
    FACEBOOK_REDIRECT_URI = 'http://skimreads.com/oauth/facebook/authenticate'
FACEBOOK_SCOPE = ','.join(['email', 'publish_actions'])

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Default @login_required login_url
LOGIN_URL = '/login/'

# Managers
MANAGERS = ADMINS

# Absolute filesystem path to the directory that will hold user-uploaded files.
if DEV:
    MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 
        'media')).replace('\\', '/').replace('\%s' % project_name, '/%s' % project_name)
else:
    MEDIA_ROOT = os.path.dirname(__file__).replace('\\','/') + '/../media'

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'

IMAGE_URL = 'img/users/'

IMAGE_READ_URL = 'img/reads/'

MEDIA_IMAGE = MEDIA_URL + IMAGE_URL

MEDIA_IMAGE_READ = 'media/' + IMAGE_READ_URL

MEDIA_IMAGE_ROOT = MEDIA_ROOT + '/' + IMAGE_URL

MEDIA_IMAGE_READ_ROOT = MEDIA_ROOT + '/' + IMAGE_READ_URL

MEDIA_AWS = 'http://s3.amazonaws.com/%s%s' % (
    BUCKET_NAME, MEDIA_IMAGE)

MEDIA_AWS_READ = 'http://s3.amazonaws.com/%s/%s' % (
    BUCKET_NAME, MEDIA_IMAGE_READ)

# Memcachier
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

CACHES = {
  'default': {
    'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
    'TIMEOUT': 500,
    'BINARY': True,
    'OPTIONS': {
        'tcp_nodelay': True,
        'remove_failed': 4
    }
  }
}

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Message
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'skimreads.urls'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '_7x$^#(o6jwcp(x7$20d@#00cb8au6#70burr2olrt9npla+y4'

# Session
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Absolute path to the directory static files should be collected to.
if DEV:
    STATIC_ROOT = ''
else:
    STATIC_ROOT = os.path.dirname(
        __file__).replace('\\','/') + '/../static'

# URL prefix for static files.
if DEV:
    STATIC_URL = '/static/'
else:
    STATIC_URL = 'http://s3.amazonaws.com/skimreads/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 
        'static')).replace('\\', '/').replace('\%s' % project_name, '/%s' % project_name),
)

# List of finder classes that know how to find static files in
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    # other finders
    'compressor.finders.CompressorFinder',
)

# static file server
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    # Pass request.user through RequestContext
    'django.core.context_processors.request',
    # Pass messages through RequestContext
    'django.contrib.messages.context_processors.messages',
    # Pass MEDIA_URL through RequestContext
    'django.core.context_processors.media',
)

TEMPLATE_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 
        'templates')).replace('\\', '/').replace('\%s' % project_name, '/%s' % project_name),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'skimreads.wsgi.application'

# Django Compressor Amazon S3
COMPRESS_URL = 'http://s3.amazonaws.com/skimreads/'
COMPRESS_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Installed apps
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'haystack',
)

# Installed utility apps
INSTALLED_APPS += (
    # Apps
    'compressor',
    'south',
    'storages',
)

# Installed skimread apps
INSTALLED_APPS += (
    'admins',
    'comments',
    'favorites',
    'follows',
    'globaltags',
    'notes',
    'notifications',
    'oauth',
    'readings',
    'replies',
    'sessions',
    'tags',
    'usermessages',
    'users',
    'votes',
)

# Haystack
# Solr
if DEV and not DEV:
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': 'http://127.0.0.1:8080/solr/',
        }
    }
else:
    HAYSTACK_URL = os.environ.get('WEBSOLR_URL', '')
    HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
            'URL': HAYSTACK_URL,
        }
    }
# Whoosh
#HAYSTACK_CONNECTIONS = {
#    'default': {
#        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
#        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
#    }
#}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}