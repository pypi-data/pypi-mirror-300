import os
import logging

logger = logging.getLogger(__name__)


def list_object_count_and_bytes_gs(bucket_name):
    """list gcs bucket objects size and count

    1. `pip install google-cloud-storage`
    2. `GOOGLE_APPLICATION_CREDENTIALS` must be set

    Args:
        bucket_name (string): bucket name

    Returns:
        dict: { "bytes": storage_bytes_value, "count": storage_count_value }
    """
    import time
    try:
        from google.cloud import storage
    except ImportError:
        logger.error("Failed to import 'google.cloud.storage'. Please ensure it's installed.")
        storage = None

    if storage is None:
        logger.error("Google Cloud Storage library not available.")
        return None

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)

    total_bytes = 0
    total_count = 0
    for blob in bucket.list_blobs():
        total_bytes += blob.size
        total_count += 1

    return {"bytes": total_bytes, "count": total_count}


def list_object_count_and_bytes_az(bucket_name):
    """list azure blob storage objects size and count

    1. `pip install azure-storage-blob`
    2. `AZURE_STORAGE_CONNECTION_STRING` must be set

    Args:
        bucket_name (string): bucket name

    Returns:
        dict: { "bytes": storage_bytes_value, "count": storage_count_value }
    """
    import os
    from azure.storage.blob import BlobServiceClient

    blob_service_client = BlobServiceClient.from_connection_string(
        os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    )

    container_client = blob_service_client.get_container_client(bucket_name)

    total_size = 0
    total_count = 0
    for blob in container_client.list_blobs():
        total_size += blob.size
        total_count += 1

    return {"bytes": total_size, "count": total_count}


def list_object_count_and_bytes_s3(bucket_name):
    """list s3 bucket objects size and count

    1. `pip install boto3`
    2.  `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` must be set

    Args:
        bucket_name (string): bucket name

    Returns:
        dict: { "bytes": storage_bytes_value, "count": storage_count_value }
    """
    import boto3

    s3 = boto3.resource("s3")

    bucket = s3.Bucket(bucket_name)

    total_size = 0
    total_count = 0
    for obj in bucket.objects.all():
        total_size += obj.size
        total_count += 1

    return {"bytes": total_size, "count": total_count}


def list_object_count_and_bytes_oss(bucket_name):
    """list oss bucket objects size and count

    1. `pip install oss2`
    2. `OSS_ACCESS_KEY_ID`, `OSS_ACCESS_KEY_SECRET` must be set

    Args:
        bucket_name (string): bucket name

    Returns:
        dict: { "bytes": storage_bytes_value, "count": storage_count_value }
    """
    import oss2

    auth = oss2.Auth(
        os.environ["OSS_ACCESS_KEY_ID"], os.environ["OSS_ACCESS_KEY_SECRET"]
    )
    bucket = oss2.Bucket(auth, os.environ['OSS_ENDPOINT'] or "oss-cn-hangzhou.aliyuncs.com", bucket_name)

    total_size = 0
    total_count = 0
    for obj in oss2.ObjectIterator(bucket):
        total_size += obj.size
        total_count += 1

    return {"bytes": total_size, "count": total_count}


def list_object_count_and_bytes_minio(bucket_name):
    """list minio bucket objects size and count

    1. `pip install minio`
    2. `MINIO_ENDPOINT`, `MINIO_ACCESS_KEY`, `MINIO_SECRET_KEY` must be set

    Args:
        bucket_name (string): bucket name

    Returns:
        dict: { "bytes": storage_bytes_value, "count": storage_count_value }
    """
    import os
    import minio

    client = minio.Minio(
        os.environ["MINIO_ENDPOINT"],
        access_key=os.environ["MINIO_ACCESS_KEY"],
        secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=False,
    )

    total_size = 0
    total_count = 0
    for obj in client.list_objects(bucket_name, recursive=True):
        total_size += obj.size
        total_count += 1

    return {"bytes": total_size, "count": total_count}
