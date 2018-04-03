from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '123456abC',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

DEBUG = True