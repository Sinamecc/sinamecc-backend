from .base import *
from django.utils.translation import gettext_lazy as _
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sinamecc-dev',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

DEBUG = True


# TODO:
# - Set duration time for signed url
BASE_DIR_FRONTEND = 'http://localhost:4200'
AWS_STORAGE_BUCKET_NAME = 'sinamecc-dev'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_PRIVATE_MEDIA_LOCATION = 'sinamecc_file_upload'
PRIVATE_FILE_STORAGE = 'general.storages.PrivateMediaStorage'

AWS_QUERYSTRING_AUTH = True

ALLOWED_HOSTS = ['*']



LANGUAGE_CODE = "en-US"

USE_I18N = True