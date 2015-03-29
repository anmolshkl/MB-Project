"""
Django settings for mentorbuddy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SETTINGS_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.join(SETTINGS_DIR, os.pardir)

PROJECT_PATH = os.path.abspath(PROJECT_PATH)

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')

STATIC_PATH = os.path.join(PROJECT_PATH,'static')

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
    'apps.mentor',
    'apps.mentee',
    'apps.user',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.github',
    'crispy_forms',
    'haystack',
    'whoosh',
    #'debug_toolbar',
)


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
    #"apps.user.backends.EmailAuthBackend",

)
 
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",

    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
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

#sameer

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
    # 'aws_rds': {
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'vnit_alumni',
        # 'USER': 'master',
        # 'PASSWORD': 'A!p_Mast3r',
        # 'HOST': 'vnit-alumni.cgjesgyaqngr.ap-southeast-1.rds.amazonaws.com',
        # 'PORT': '3306',
    # },
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

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media') # Absolute path to the media directory




# Login urls
LOGIN_URL          = '/user/login/'
LOGOUT_URL         = '/user/logout/'
LOGIN_REDIRECT_URL = '/user/' #-adapter will provide the login_redirect_url,but adapter doesn't support

SOCIALACCOUNT_PROVIDERS = \
    { 'google':
        { 'SCOPE': ['profile', 'email',],
          'AUTH_PARAMS': { 'access_type': 'online' } }}

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'SCOPE': ['email', 'publish_stream','public_profile','user_birthday','user_education_history','user_location'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',
        'LOCALE_FUNC': lambda request: 'zh_CN',
        'VERIFIED_EMAIL': False},
    
    'linkedin':
        {'SCOPE': ['r_emailaddress','r_fullprofile','r_basicprofile'],
               'PROFILE_FIELDS': ['id',
                                 'first-name',
                                 'last-name',
                                 'date-of-birth',
                                 'email-address',
                                 'picture-url',
                                 'headline',
                                 'location',
                                 'industry',
                                 'summary',
                                 'languages',
                                 'skills',
                                 'phone-numbers ',
                                 'positions',
                                 'educations',
                                 'publications',    
                                 'public-profile-url']}}
'''
SOCIALACCOUNT_PROVIDERS = \
    {'twitter':
       {'SCOPE': ['email', 'publish_stream','public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',
        'LOCALE_FUNC': lambda request: 'zh_CN',
        'VERIFIED_EMAIL': False}}
'''


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_HOST_USER = 'anmol@mentorbuddy.in'
EMAIL_HOST_PASSWORD = '8zryfcgve33k'
EMAIL_PORT = 587

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION  = "none" #later change to mandatory
ACCOUNT_LOGOUT_REDIRECT_URL = "/user/"
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
#custom adapter to override login behavior and associate different social profiles with same email,with same user
SOCIALACCOUNT_ADAPTER = 'mentorbuddy.adapters.adapter.SocialLoginAdapter'

#Crispy form
CRISPY_TEMPLATE_PACK = 'bootstrap3'



#SITE URL 
SITE_URL = "http://localhost:8000/"

#Use Time Zones
USE_TZ = True

VISITOR_INFO_GEOIP_DATABASE_PATH = os.path.join(BASE_DIR, 'apps', 'django_visitor_information', 'static', 'GeoLiteCity.dat')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR,'debug.log'),
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