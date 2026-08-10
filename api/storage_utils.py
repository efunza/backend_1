import os
from urllib.parse import urljoin

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    boto3 = None

from django.conf import settings


def get_s3_client():
    if boto3 is None:
        raise RuntimeError("boto3 is required for S3 presigned helpers")
    return boto3.client(
        's3',
        aws_access_key_id=getattr(settings, 'AWS_ACCESS_KEY_ID', None),
        aws_secret_access_key=getattr(settings, 'AWS_SECRET_ACCESS_KEY', None),
        region_name=getattr(settings, 'AWS_S3_REGION_NAME', None)
    )


def generate_presigned_get(key, expires_in=3600):
    """Return a presigned URL for GET (download) for S3 objects."""
    if not getattr(settings, 'USE_S3', False):
        # If not using S3, return a local MEDIA URL
        base = getattr(settings, 'MEDIA_URL', '/media/')
        return urljoin(base, key)

    client = get_s3_client()
    bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
    try:
        url = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expires_in
        )
        return url
    except ClientError:
        return None


def generate_presigned_post(key, expires_in=3600, content_type=None):
    """Return the presigned POST data (url and fields) for direct uploads to S3."""
    if not getattr(settings, 'USE_S3', False):
        raise RuntimeError("Presigned uploads are only supported when USE_S3=True")

    client = get_s3_client()
    bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
    fields = {}
    conditions = []
    if content_type:
        fields['Content-Type'] = content_type
        conditions.append({'Content-Type': content_type})

    try:
        post = client.generate_presigned_post(
            Bucket=bucket,
            Key=key,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expires_in,
        )
        return post
    except ClientError:
        return None
