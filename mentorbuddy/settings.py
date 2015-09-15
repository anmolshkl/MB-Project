from __future__ import absolute_import
from datetime import timedelta  # topmost line


"""
Django settings for mentorbuddy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import warnings
import djcelery

djcelery.setup_loader()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SETTINGS_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)

PROJECT_PATH = os.path.abspath(PROJECT_PATH)

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')

STATIC_PATH = os.path.join(PROJECT_PATH, 'static')

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_PATH,
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o22!xyp&^cmbm0399^@6(qoe9yv#42200(@ajjea-)+*9&x70r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # The Django sites framework is required
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'apps.mentor',
    'apps.mentee',
    'apps.user',
    'crispy_forms',
    'haystack',
    'whoosh',
    'widget_tweaks',
    'djcelery',
    'kombu.transport.django',
    # 'debug_toolbar',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    # 'apps.user.customScope.CustomFacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    # 'apps.user.customScope.CustomFacebookOAuth2',

    'social.backends.linkedin.LinkedinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.django_visitor_information.middleware.TimezoneMiddleware',
    'apps.django_visitor_information.middleware.VisitorInformationMiddleware',

)

SITE_ID = 1

ROOT_URLCONF = 'mentorbuddy.urls'

WSGI_APPLICATION = 'mentorbuddy.wsgi.application'

# sameer

# Haystack configuration

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'localhost': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mb_db2',
        'USER': 'mentorbuddy',
        'PASSWORD': 'mentorbuddy',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}
# Django NEEDS a 'default'. Do change the following in production!
DATABASES['default'] = DATABASES['localhost']

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, '../staticfiles/')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')  # Absolute path to the media directory

# Login urls
# LOGIN_URL = '/user/login/'
LOGOUT_URL = '/user/logout/'
LOGIN_REDIRECT_URL = '/user/'  # -adapter will provide the login_redirect_url,but adapter doesn't support

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'mentorbuddy'
EMAIL_HOST_PASSWORD = 'MB4abhijeet'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'apps.user.views.save_social_profile'
    # 'profiles.pipeline.user_details'
)

# Python-social-auth settings
SOCIAL_AUTH_FACEBOOK_SCOPE = ['public_profile', 'user_birthday', 'user_education_history', 'user_location', 'email']
SOCIAL_AUTH_FACEBOOK_KEY = '713549365387916'
SOCIAL_AUTH_FACEBOOK_SECRET = '5fd7cd3b9958b979647df997b5b27c8e'

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '745226397307-sktc3grus53u160q3icthf5s51ukijke.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Qg4q0dAsipUqAuYa2TOVnMGF'

SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '75v6ppasybk7zd'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'WJjgPEsGW7NSCVCD'
# Add the fields so they will be requested from linkedin.
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = ['email-address', 'headline', 'industry', 'location', 'summary',
                                               'picture-url', 'public-profile-url', 'date-of-birth']
# Arrange to add the fields to UserSocialAuth.extra_data
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [('id', 'id'),
                                          ('firstName', 'first_name'),
                                          ('lastName', 'last_name'),
                                          ('emailAddress', 'email_address'),
                                          ]

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/login/'


# Crispy form
CRISPY_TEMPLATE_PACK = 'bootstrap3'



# SITE URL
#SITE_URL = "http://127.0.0.1:8000/"
SITE_URL = "http://mentorbuddy.in/"

#Use Time Zones
USE_TZ = True

VISITOR_INFO_GEOIP_DATABASE_PATH = os.path.join(BASE_DIR, 'apps', 'django_visitor_information', 'static',
                                                'GeoLiteCity.dat')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

warnings.filterwarnings(
    'error', r"DateTimeField .* received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields')

DATETIME_INPUT_FORMATS = (
    '%m-%d-%Y'
)

BROKER_URL = "amqp://ubuntu:m3ntorbuddy@localhost:5672/host1"
# BROKER_URL = 'django://'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'UTC'

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

CELERYBEAT_SCHEDULE = {
    "notify-upcoming-calls": {
        "task": "apps.user.tasks.notify",
        "schedule": timedelta(minutes=30),
    }
}
