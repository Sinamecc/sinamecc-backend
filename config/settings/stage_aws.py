from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sinamecc_stage',
        'USER': 'sinamecc_dba',
        'PASSWORD': 'wwnRyDlf4v9odUa',
        'HOST': 'sinamecc.copuo03vfifp.us-east-2.rds.amazonaws.com',
        'PORT': 5432,
    }
}

DEBUG = False
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = ('stage.sinamecc-minae.com','ec2-13-58-84-4.us-east-2.compute.amazonaws.com','ip-172-31-40-51.us-east-2.compute.internal')

MEDIA_ROOT = "/var/www/app/sinamecc-uploads"
