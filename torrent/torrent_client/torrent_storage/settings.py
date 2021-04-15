"""
Django settings for torrent_storage project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os


def ensure_dirpath_existence(paths):
    for path in paths:
        if MEDIA_ROOT not in path:
            path = os.path.join(MEDIA_ROOT, path)
        if os.path.isfile(path):
            dirpath = os.path.dirname(path)
        else:
            dirpath = path

        if not os.path.exists(dirpath):
            os.makedirs(dirpath)




# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPLOYMENT_ENV_DEV = 'development'
DEPLOYMENT_ENV_PROD = 'production'
DEPLOYMENT_ENV_STAG = 'staging'

DEPLOYMENT_ENV = os.environ['DEPLOYMENT_ENVIRONMENT']

# s3 stuff
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, 'media')
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

TRANSMISSION_ADDRESS = '127.0.0.1'
TRANSMISSION_PORT = 9091
TRANSMISSION_PASSWORD = '{fd0b98f556eb42f17ba2ac30500be3f37a0d88a40nyzXz2s'
TRANSMISSION_USERNAME = 'oben'
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'logs.txt')
PROJECT_PAI_DIR = os.path.expanduser('~/projectpai')
PROJECT_PAI_DATA_DIR = os.path.join(PROJECT_PAI_DIR, 'data')
MEDIA_ROOT = '/' + DEPLOYMENT_ENV
# the following paths are relative to the MEDIA_ROOT
BITTORRENT_TORRENT_FILE_DIR = os.path.join('torrent', 'torrent_file')
BITTORRENT_TORRENT_DATA_DIR = os.path.join('torrent','torrent_data')
FILE_PATH = os.path.join('torrent', 'files')

BLOCKCHAIN_TYPE = os.environ['BLOCKCHAIN_TYPE']

# TODO rename; this is some really poor naming
class PaiPdp2Protocol_Paicoin:
    # HEADER
    PAI_DELIMITER_SZ = 1  #
    VERSION_SZ = 1
    RESERVED_SZ = 6
    # PAYLOAD
    OPERATION_SZ = 1
    STORAGE_METHOD_SZ = 1
    OP1_SZ_SZ = 1
    OP1_SZ = 32

    OP2_SZ_SZ = 1
    OP2_SZ = 32
    CHECKSUM_SZ = 4


class PaiPdp2Protocol_Bitcoin(PaiPdp2Protocol_Paicoin):
    # HEADER
    # Since we only have 40 bytes we leave out the header to fit the rest in.
    PAI_DELIMITER_SZ = 0
    VERSION_SZ = 0
    RESERVED_SZ = 0

    # We additionally leave  out the checksum.
    CHECKSUM_SZ = 0

    OP_RETURN_SIZE = 40

    OP1_SZ = OP_RETURN_SIZE - PAI_DELIMITER_SZ - VERSION_SZ - PaiPdp2Protocol_Paicoin.OPERATION_SZ \
             - PaiPdp2Protocol_Paicoin.STORAGE_METHOD_SZ - PaiPdp2Protocol_Paicoin.OP1_SZ_SZ \
             - PaiPdp2Protocol_Paicoin.OP2_SZ_SZ - PaiPdp2Protocol_Paicoin.OP2_SZ - CHECKSUM_SZ


if BLOCKCHAIN_TYPE.lower() == 'bitcoin':
    # Bitcoin OP_RETURN size actually changed from (in units of bytes):
    # 80 -> 40 -> 80 -> 83
    # I mistakenly thought it was still 40 for some reason.
    # Leaving this here to fix later:
    # TODO: fix
    PAI_PDP2_PROTOCOL = PaiPdp2Protocol_Paicoin
elif BLOCKCHAIN_TYPE.lower() == 'paicoin':
    PAI_PDP2_PROTOCOL = PaiPdp2Protocol_Paicoin
else:
    raise Exception(f'BLOCKCHAIN Type "{BLOCKCHAIN_TYPE}" not recognized.')

external_paths = [os.path.dirname(LOG_FILE), PROJECT_PAI_DIR,
                  PROJECT_PAI_DATA_DIR, BITTORRENT_TORRENT_FILE_DIR,
                  BITTORRENT_TORRENT_DATA_DIR, FILE_PATH]

ensure_dirpath_existence(external_paths)

NEW_INFO_HASH = os.environ['NEW_INFO_HASH_DELIM']
NULL_UUID = '99999999-9999-9999-9999-999999999999'

SITE_URL = r'http://torrentclient:8000/'
BITTORRENT_TRACKER_ADD_TORRENT_CMD = ("transmission-remote -n"
                                      "'%s:%s' -a " % (TRANSMISSION_USERNAME,
                                                       TRANSMISSION_PASSWORD))
tracker_host = os.environ['TORRENT_TRACKER_HOST']
tracker_port = os.environ['TORRENT_TRACKER_PORT']
BACKEND_TRACKER_URL = "http://%s:%s/" % (tracker_host, tracker_port)

external_tracker_host = os.environ['EXTERNAL_TORRENT_TRACKER_HOST']
external_tracker_port = os.environ['EXTERNAL_TORRENT_TRACKER_PORT']

opentracker_host = os.environ['TORRENT_TRACKER_HOST']
opentracker_port = os.environ['OPENTRACKER_PORT']
TRACKER_URL = "http://%s:%s/" % (opentracker_host, opentracker_port)
EXTERNAL_TRACKER_URL = "http://%s:%s/" % (external_tracker_host, external_tracker_port)
TRACKERS = (TRACKER_URL + 'announce',
            'http://%s:%s/announce' % ('localhost', opentracker_port),
            EXTERNAL_TRACKER_URL+'/announce')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gq7@avb5fnr2b9&e0-$3bww0wsdpoq8soa441tg*3h9=!mt&p1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['torrentclient']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'file_api.apps.FileApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'torrent_storage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'torrent_storage.wsgi.application'

db_host = os.environ['SQL_HOST']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['SQL_USER'],
        'PASSWORD': os.environ['SQL_PASS'],
        'HOST': db_host,
        'PORT': os.environ['SQL_PORT']
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

