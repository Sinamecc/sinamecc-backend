from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
    }
}

DEBUG = True

# TODO:
# - Set duration time for signed url

AWS_STORAGE_BUCKET_NAME = 'sinamecc-dev'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_ACCESS_KEY_ID = 'CHANGE ME'
AWS_SECRET_ACCESS_KEY = 'CHANGE ME'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_PRIVATE_MEDIA_LOCATION = 'sinamecc_file_upload'
PRIVATE_FILE_STORAGE = 'general.storages.PrivateMediaStorage'

AWS_QUERYSTRING_AUTH = True