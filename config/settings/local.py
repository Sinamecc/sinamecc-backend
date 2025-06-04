from .base import *

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
## settings S3 Storage
AWS_STORAGE_BUCKET_NAME = "sinamecc-dev"
AWS_QUERYSTRING_AUTH = True
AWS_QUERYSTRING_EXPIRE = 60
AWS_S3_REGION_NAME = "us-east-2"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": 5432,
    }
}

STORAGES = {
    "default": {
        "BACKEND": "core.aws.s3.S3StorageDefault",
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
DEBUG = True

FRONTEND_URL = "http://localhost:4200"

# TODO:
# - Set duration time for signed url
# O el endpoint correspondiente a tu región


ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:4200",
]
