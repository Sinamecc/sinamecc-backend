from html import escape
from typing import Any

from storages.backends.s3boto3 import S3Boto3Storage

# class S3StorageGeneral(S3Boto3Storage):
#     ...

# class S3StorageDefault(S3StorageGeneral):
#     bucket_name = ''
#     custom_domain = '{}.s3.amazonaws.com'.format(bucket_name)
#     location = 'default'

# class S3StorageStaticFiles(S3StorageGeneral):
#     bucket_name = ''
#     custom_domain = '{}.s3.amazonaws.com'.format(bucket_name)
#     location = 'static'
    
# class S3StorageMediaFiles(S3StorageGeneral):
#     bucket_name = ''
#     custom_domain = '{}.s3.amazonaws.com'.format(bucket_name)
#     location = 'media'



class S3StorageGeneral(S3Boto3Storage):
    """Override some upload parameters, such as ContentDisposition header."""

    def _get_write_parameters(self, name: str, content: bytes) -> dict[str, Any]:
        ## REF : https://stackoverflow.com/questions/43208401/add-dynamic-content-disposition-for-file-namesamazon-s3-in-python
        params = super()._get_write_parameters(name, content)
        original_name = getattr(content, 'name', None)
        if original_name and name != original_name:
            content_disposition = f'attachment; filename="{escape(original_name)}"'
            params['ContentDisposition'] = content_disposition
        return params