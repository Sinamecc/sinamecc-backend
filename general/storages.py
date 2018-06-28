from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class PrivateMediaStorage(S3Boto3Storage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

class S3Storage():
    def __init__(self):
        self.storage = PrivateMediaStorage()

    def get_file(self, file_path):
        signed_url = None
        if (self.storage.exists(file_path)):
            # get signed url
            signed_url = self.storage.url(file_path)

        # handle exception
        return signed_url