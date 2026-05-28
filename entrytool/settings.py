# Django settings for entrytool project.
import os

from django.utils.translation import gettext_lazy as _


def str2bool(v):
    if not v: return False
    return v.lower() in ("true", "1")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['OPAL_SECRET_KEY']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str2bool(os.environ.get('DEBUG', 'false'))
COMPRESS_ENABLED = False

#ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".honeur.org"]
ALLOWED_HOSTS = ["*"]

LOGOUT_REDIRECT_URL = '/ecrf'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv('DJANGO_ROOT_LOG_LEVEL', 'WARNING'),
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

auth_backends = ['django.contrib.auth.backends.ModelBackend', ]

enable_ldap = str2bool(os.environ.get('OPAL_ENABLE_LDAP', 'false'))
enable_user_db = str2bool(os.environ.get('OPAL_ENABLE_USER_DB', 'false'))
if enable_ldap:
    auth_backends = ['django_auth_ldap.backend.LDAPBackend', 'django.contrib.auth.backends.ModelBackend', ]
    import logging

    logger = logging.getLogger('django_auth_ldap')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)
    import ldap
    from django_auth_ldap.config import LDAPSearch

    AUTH_LDAP_SERVER_URI = os.environ["OPAL_LDAP_SERVER_URI"]
    AUTH_LDAP_BIND_DN = os.environ["OPAL_LDAP_BIND_DN"]
    AUTH_LDAP_BIND_PASSWORD = os.environ["OPAL_LDAP_BIND_PASSWORD"]
    AUTH_LDAP_USER_SEARCH = LDAPSearch(os.environ["OPAL_LDAP_USER_SEARCH_DN"], ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
elif enable_user_db:
    auth_backends = ['entrytool.auth.backend.HoneurUserDatabaseAuthentication',
                     'django.contrib.auth.backends.ModelBackend', ]

AUTHENTICATION_BACKENDS = auth_backends

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "statici18n",
    "rest_framework",
    "rest_framework.authtoken",
    "compressor",
    "opal",
    "opal.core.search",
    "opal.core.pathway",
    "reversion",
    #    "opal.core.referencedata",
    "entrytool",
    "plugins.conditions.cll",
    "plugins.conditions.mm",
    # 'languages',
    "django.contrib.admin",
    "plugins.data_load"
]

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "opal.middleware.AngularCSRFRename",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "opal.middleware.DjangoReversionWorkaround",
    "reversion.middleware.RevisionMiddleware",
    # 'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = "entrytool.urls"
APPEND_SLASH = False

LOADERS = [
    (
        # TODO: Django 1.11 makes turns this loader on by default, so
        # this section and `debug` can be removed then.
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]
if DEBUG:
    LOADERS = (
        "django.template.loaders.filesystem.Loader",
        "django.template.loaders.app_directories.Loader",
    )

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_PATH, "templates")],
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "opal.context_processors.settings",
                "opal.context_processors.models",
                "opal.core.pathway.context_processors.pathways",
            ],
            "loaders": LOADERS,
        },

    },
]

WSGI_APPLICATION = "entrytool.wsgi.application"

DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ['OPAL_DB_NAME'],
            "USER": os.environ['OPAL_DB_USER'],
            "PASSWORD": os.environ['OPAL_DB_PASSWORD'],
            "HOST": os.environ['OPAL_DB_HOST'],
            "PORT": os.environ['OPAL_DB_PORT'],
            'OPTIONS': {
                'options': '-c search_path=opal'
            },
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGES = (
    ("en-us", _("English")),
    ("es", _("Spanish")),
    ("he", _("Hebrew")),
)

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = "/assets/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "assets")
STATICFILES_DIRS = [
    os.path.join(PROJECT_PATH, "static"),
]
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# Django Site identifier
SITE_ID = 1

# Date and Time Formatting
# https://docs.djangoproject.com/en/1.10/ref/settings/#date-format
DATETIME_FORMAT = "d/m/Y H:i:s"
DATETIME_INPUT_FORMATS = ["%d/%m/%Y %H:%M:%S"]
DATE_FORMAT = "d/m/Y"
DATE_INPUT_FORMATS = ["%d/%m/%Y"]
TIME_FORMAT = "H:i:s"

# Emails
# https://docs.djangoproject.com/en/1.10/ref/settings/#email-backend
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
if not DEBUG:
    EMAIL_HOST_USER = os.environ.get("SENDGRID_USERNAME", "")
    EMAIL_HOST = "smtp.sendgrid.net"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ.get("SENDGRID_PASSWORD", "")
else:
    EMAIL_PORT = 1025
    EMAIL_HOST = "localhost"

# HTTPS support
# https://docs.djangoproject.com/en/1.10/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Sessions
# https://docs.djangoproject.com/en/1.10/topics/http/sessions/#browser-length-sessions-vs-persistent-sessions
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# CSRF
# https://docs.djangoproject.com/en/1.10/ref/settings/#csrf-cookie-name
CSRF_COOKIE_NAME = "XSRF-TOKEN"
CSRF_FAILURE_VIEW = "opal.views.csrf_failure"

# Rest Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    )
}

# ========== OPAL ==========
# Testing
COVERAGE_EXCLUDE_MODULES = (
    "entrytool.migrations",
    "entrytool.tests",
    "entrytool.local_settings",
    "opal.migrations",
    "opal.tests",
    "opal.wsgi",
)

OPAL_LOG_OUT_MINUTES = 15
OPAL_LOG_OUT_DURATION = OPAL_LOG_OUT_MINUTES * 60 * 1000

# OPAL_EXTRA_HEADER = ''
# OPAL_EXTRA_APPLICATION = ''

# Uncomment this if you want to swap the logo used by this application.
# http://opal.openhealthcare.org.uk/docs/v0.10.0/reference/settings/#opal_logo_path
OPAL_LOGO_PATH = 'img/HONEUR_logo.png'
OPAL_FAVICON_PATH = 'img/HONEUR_favicon.png'

# Enable/Disable autocomplete from navbar search
OPAL_AUTOCOMPLETE_SEARCH = False

INTEGRATING = False

# OPAL-required Django settings you should edit
CONTACT_EMAIL = []
DEFAULT_FROM_EMAIL = "hello@example.com"
DEFAULT_DOMAIN = "http://entrytool.com/"

OPAL_DEFAULT_SEARCH_FIELDS = [
    "demographics__external_identifier",
    "demographics__hospital_number",
    "id"
]

# This list acts as a whitelist for the context processor
OPAL_SETTING_NAMES = [
    'OPAL_BRAND_NAME',
    'OPAL_THEME',
]

# ========== PROJECT ==========
OPAL_BRAND_NAME = "Data Entry Tool"
VERSION_NUMBER = "0.2"

if os.environ.get('HEROKU_SLUG_COMMIT'):
    VERSION_NUMBER = '{} ({})'.format(VERSION_NUMBER, os.environ.get('HEROKU_SLUG_COMMIT'))

# if you want sass, uncomment the below and gem install sass
# COMPRESS_PRECOMPILERS = (
#     ('text/x-scss', 'sass --scss {infile} {outfile}'),
# )
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

# A patient who has not been updated in {LOST_TO_FOLLOW_UP_DAYS_SINCE} days
# will appear on the Lost To Follow-Up page
LOST_TO_FOLLOW_UP_DAYS_SINCE = 180

# The function called by entrytool.api.create
# manage.py load_data.
# It takes the file and then returns the errors
UPLOAD_FROM_FILE_FUNCTION = 'plugins.conditions.mm.load_data.load_data'

try:
    from entrytool.local_settings import *
except ImportError:
    pass
