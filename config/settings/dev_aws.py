from .base import *
import environ

env = environ.Env(DEBUG=(bool, False))
env.read_env() ## load variable env config/settings/.env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DATABASE_NAME', default='sinamecc_dev_2020'),
        'USER': env.str('DATABASE_USER'),
        'PASSWORD': env.str('DATABASE_PASSWORD')
        'HOST': env.str('DATABASE_NAME', default='sinamecc.copuo03vfifp.us-east-2.rds.amazonaws.com'),
        'PORT': 5432,
    }
}

DEBUG = True
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = ('dev.sinamecc.go.cr','ec2-18-218-214-170.us-east-2.compute.amazonaws.com','ip-172-31-20-146.us-east-2.compute.internal')

MEDIA_ROOT = "/var/www/app/sinamecc-uploads"

AWS_STORAGE_BUCKET_NAME = 'sinamecc-dev'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_PRIVATE_MEDIA_LOCATION = 'sinamecc_file_upload'
PRIVATE_FILE_STORAGE = 'general.storages.PrivateMediaStorage'

AWS_QUERYSTRING_AUTH = True
