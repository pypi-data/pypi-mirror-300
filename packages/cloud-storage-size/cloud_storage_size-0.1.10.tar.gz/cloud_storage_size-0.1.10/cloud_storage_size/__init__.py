import os
import logging
from urllib.parse import urlparse
from .sdk_client import (
    list_object_count_and_bytes_az,
    list_object_count_and_bytes_s3,
    list_object_count_and_bytes_oss,
    list_object_count_and_bytes_minio,
    list_object_count_and_bytes_gs,
)
from .gs_query_metrics import query_google_cloud_minitoring
from .rclone import size, is_using_rclone_connection_strings

logger = logging.getLogger(__name__)


def get_bucket_objects_count_and_bytes(bucket_uri, **kwargs):
    """get cloud storage bucket objects count and bytes

    Args:
        bucket_uri (cloud storage bucket uri):
            cloud storage bucket uri, e.g. "gs://bucket_name", "s3://bucket_name", "oss://bucket_name"
        kwargs:    
            engine (str, optional):
                cloud storage engine, ["auto", "rclone", "metrics", "sdk"]. Defaults to "rclone",
                metrics only support google cloud storage.
            project_id (str, optional):
                google cloud project id, required if engine is "metrics".

    Returns:
        dict: { "bytes": storage_bytes_value, "count": storage_count_value }
    """
    parsed_url = urlparse(bucket_uri)
    scheme = parsed_url.scheme
    bucket_name = parsed_url.netloc
    engine = kwargs.get("engine", "auto")

    def process_by_metrics():
        try:
            if scheme != "gs":
                raise ValueError("metrics only support google cloud storage")
            project_id = kwargs.get("project_id", None)
            if project_id is None:
                project_id = os.environ.get("RCLONE_CONFIG_MYREMOTE_PROJECT_NUMBER", None)
            if project_id is None:
                raise ValueError("project_id is required")
            
            return query_google_cloud_minitoring(project_id, bucket_name)
        except Exception as e:
            logger.error("query_google_cloud_minitoring error: %s", e)
            return None

    def process_by_rclone(bucket_uri, **kwargs):
        try:
            return size(bucket_uri, **kwargs)
        except Exception as e:
            logger.error("rclone size error: %s", e)
            return None

    def process_by_sdk():
        try:
            if scheme == "gs":
                return list_object_count_and_bytes_gs(bucket_name)
            elif scheme == "s3":
                return list_object_count_and_bytes_s3(bucket_name)
            elif scheme == "oss":
                return list_object_count_and_bytes_oss(bucket_name)
            elif scheme == "minio":
                return list_object_count_and_bytes_minio(bucket_name)
            elif scheme == "az":
                return list_object_count_and_bytes_az(bucket_name)
            else:
                raise ValueError("unsupported scheme")
        except Exception as e:
            logger.error("sdk list_object_count_and_bytes error: %s", e)
            return None

    return_value = None

    # connection strings only support rclone
    if is_using_rclone_connection_strings(bucket_uri):
        return_value = process_by_rclone(bucket_uri, **kwargs)
        if return_value:
            return return_value

    if engine == "auto":
        if scheme == "gs":
            return_value = process_by_metrics()
        if return_value is None:
            return_value = process_by_rclone(bucket_uri, **kwargs)
        if return_value is None:
            return_value = process_by_sdk()
    elif engine == "metrics":
        return_value = process_by_metrics()
    elif engine == "rclone":
        return_value = process_by_rclone(bucket_uri, **kwargs)
    elif engine == "sdk":
        return_value = process_by_sdk()
    return return_value
