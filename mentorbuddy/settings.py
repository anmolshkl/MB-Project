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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.mentor',
    'apps.mentee',
    'apps.home',
    'south',
    'social.apps.django_app.default',
)
#here we specify all the social logins we want
AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mentorbuddy.urls'

WSGI_APPLICATION = 'mentorbuddy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'localhost': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mb_db',
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

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    STATIC_PATH,
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media') # Absolute path to the media directory

#TWITTER
SOCIAL_AUTH_TWITTER_KEY = 'R4LNGeDnrA6xUfuZHn6rcs9qY'
SOCIAL_AUTH_TWITTER_SECRET = 'UBQL0dlSeODOXHMWltGqX0vxtk4rPZBVC599yWkZMHM7KTi3yD'


#FACEBOOK
SOCIAL_AUTH_FACEBOOK_KEY = '713549365387916'
SOCIAL_AUTH_FACEBOOK_SECRET = '5fd7cd3b9958b979647df997b5b27c8e'
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

#LINKEDIN
#Fill the application key and secret in your settings:
SOCIAL_AUTH_LINKEDIN_KEY = '75v6ppasybk7zd'
SOCIAL_AUTH_LINKEDIN_SECRET = 'WJjgPEsGW7NSCVCD'

#Application Scopes(ie what all we want from Linkedin):
SOCIAL_AUTH_LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress','r_fullprofile']
SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = ['id','first-name',
                                            'last-name',
                                            'summary',
                                            'email-address',
                                            'positions',
                                            'headline',
                                            'picture-url',
                                            'site-standard-profile-request',
                                            'public-profile-url',
                                            'location',
                                            'interests',
                                            'publications',
                                            'date-of-birth',
                                            'primary-twitter-account' ,
                                            'skills',
                                            'languages',
                                            'educations']

SOCIAL_AUTH_LINKEDIN_EXTRA_DATA = [('id', 'linkedin_id'),
                                   ('emailAddress', 'email_address'),
                                   ('headline', 'tagline'),
                                   ('industry', 'industry'),
                                   ('educations', 'educations'),
                                   ('threeCurrentPositions', 'organisations'),
                                   ('threePastPositions', 'past_organisations'),
                                   ('dateOfBirth', 'date_of_birth'),
                                   ('mainAddress', 'address'),
                                   ('phoneNumbers', 'phone_numbers'),
                                   ('pictureUrl', 'profile_picture_url'),
                                   ('publicProfileUrl', 'public_profile_url'),
                                   ('location', 'location'),
                                   ('summary', 'about')]

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',  # <--- enable this one
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

# Login urls
LOGIN_URL          = '/home/login/'
LOGOUT_URL         = '/home/logout/'
LOGIN_REDIRECT_URL = '/home/'

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)