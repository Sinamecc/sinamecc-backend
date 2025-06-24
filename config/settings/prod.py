import environ

from .base import *

env = environ.Env()
env.read_env() ## load variable env config/settings/.env

DATABASES = {'default': env.db('DATABASE_URL')}

DEBUG = True
ALLOWED_HOSTS = ['*']

CORS_ALLOW_ALL_ORIGINS = True
FRONTEND_URL = env.str('FRONTEND_URL')
MEDIA_ROOT = "/var/www/app/sinamecc-uploads"

AWS_STORAGE_BUCKET_NAME = "sinamecc-dev"
AWS_QUERYSTRING_AUTH = True
AWS_QUERYSTRING_EXPIRE = 60
AWS_S3_REGION_NAME = "us-east-2"

STORAGES = {
    "default": {
        "BACKEND": "core.aws.s3.S3StorageGeneral",
        "OPTIONS": {
            "location": "content",
            "object_parameters": {
                "CacheControl": "max-age=86400",
             },
             
        },
    },
    "media": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "location": "media",
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "location": "static",
        },
    },
}