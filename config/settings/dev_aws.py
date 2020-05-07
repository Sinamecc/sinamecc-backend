from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sinamecc_dev_2020',
        'USER': 'sinamecc_dba',
        'PASSWORD': 'wwnRyDlf4v9odUa',
        'HOST': 'sinamecc.copuo03vfifp.us-east-2.rds.amazonaws.com',
        'PORT': 5432,
    }
}

DEBUG = True
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = ('dev.sinamecc.go.cr','ec2-18-218-214-170.us-east-2.compute.amazonaws.com','ip-172-31-20-146.us-east-2.compute.internal')

MEDIA_ROOT = "/var/www/app/sinamecc-uploads"

AWS_PRIVATE_MEDIA_LOCATION = "%s/media/private"
