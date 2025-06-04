# from storages.backends.s3boto3 import S3Boto3Storage


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