"""
Django settings for dron_market2 project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import django_heroku
import os
import ast
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR1 = os.path.abspath(__file__)
# BASE_DIR2 = os.path.dirname(os.path.abspath(__file__))
#
# BASE_DIR_ = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
# BASE_DIR1_ = os.path.dirname(__file__)
# BASE_DIR2_ = os.path.join(os.path.dirname(__file__), '..')
def get_bool_from_env(env_value, default_value):
    if env_value in os.environ:
        value = os.environ['env_value']
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValueError(
                '{} is an invalind value for {]'.format(value, env_value)) from e
    return default_value

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = '==oiuy-d9pdg)saw2widi+ghkusn7k0=$!#@-+l^yjf&*-l^sb'
SECRET_KEY = os.environ.get('SECRET_KEY', '==oiuy-d9pdg)saw2widi+ghkusn7k0=$!#@-+l^yjf&*-l^sb')
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = TEMPLATE_DEBUG = True
SITE_ID = 1
ALLOWED_HOSTS = ["whispering-fjord-52293.herokuapp.com"]

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'rudavinp@gmail.com'
EMAIL_HOST_PASSWORD = 'Benzol3fosfat'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
    
context_processors = [

    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'social_django.context_processors.backends',
    'social_django.context_processors.login_redirect',

]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',
    #my_apps
    'product',
    'order',
    'account',
    'dashboard',
    'core',
    'discount',
    #external_apps
    'bootstrap4',
    'django_filters',
    'mptt',
    'debug_toolbar',
    'social_django',
    'embed_video'


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'core.middleware.catalog_middleware'
]

ROOT_URLCONF = 'dron_market2.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'order.context_processors.get_cart_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'dron_market2.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'saleor',
        'USER': 'postgres',
        'PASSWORD': '3280661',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)

# DATABASES={
#     'default':db_from_env}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',

]
#new comment
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '622041767392-q5480allvhjrvechdel83qej2859pi02.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'WAxoUqpDL3G8x8cLZFi5R5rC'

SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_URL = '/account/login/'

LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'account.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/




MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles',)

STATICFILES_DIRS = (
  os.path.join(BASE_DIR, 'static', ),
)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'storage.WhiteNoiseStaticFilesStorage'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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

DEBUG_TOOLBAR_CONFIG = {
       'INTERCEPT_REDIRECTS': False,
   }

if DEBUG:
   INTERNAL_IPS = ('127.0.0.1', 'localhost',)

django_heroku.settings(locals())
