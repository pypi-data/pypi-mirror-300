import subprocess
import json
import os
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

SUPPORTED_SCHEME = ["gs", "gcs", "s3", "az", "azure", "oss"]


def is_supported_scheme(scheme):
    return scheme in SUPPORTED_SCHEME


def check_bucket_uri(bucket_uri):
    parsed_url = urlparse(bucket_uri)
    scheme = parsed_url.scheme
    is_vaild = is_supported_scheme(scheme)
    if not is_vaild:
        logger.info(f"unsupported scheme: {scheme} from [{bucket_uri}], only support {SUPPORTED_SCHEME}")
    return is_vaild


def is_using_rclone_connection_strings(conn_str):
    return conn_str.rsplit(":", 1)[0].find(":") != -1


def parse_path_uri(storage_bucket):
    parsed_url = urlparse(storage_bucket)
    scheme = parsed_url.scheme
    bucket_name = parsed_url.netloc
    blob_path = parsed_url.path.lstrip("/")
    return scheme, bucket_name, blob_path


def parse_env(scheme):
    env = {}
    if scheme == "gs" or scheme == "gcs":
        env = {
            "RCLONE_CONFIG_MYREMOTE_TYPE": "google cloud storage",
            "RCLONE_CONFIG_MYREMOTE_SERVICE_ACCOUNT_FILE": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_SERVICE_ACCOUNT_FILE", None
            ),
            "RCLONE_CONFIG_MYREMOTE_PROJECT_NUMBER": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_PROJECT_NUMBER", None
            ),
            "RCLONE_CONFIG_MYREMOTE_LOCATION": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_LOCATION", "us-central1"
            ),
            "RCLONE_CONFIG_MYREMOTE_OBJECT_ACL": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_OBJECT_ACL", "private"
            ),
            "RCLONE_CONFIG_MYREMOTE_BUCKET_ACL": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_BUCKET_ACL", "private"
            ),
        }
    elif scheme == "s3":
        env = {
            "RCLONE_CONFIG_MYREMOTE_TYPE": "s3",
            "RCLONE_CONFIG_MYREMOTE_PROVIDER": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_PROVIDER", "AWS"
            ),
            "RCLONE_CONFIG_MYREMOTE_ACCESS_KEY_ID": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_ACCESS_KEY_ID", None
            ),
            "RCLONE_CONFIG_MYREMOTE_SECRET_ACCESS_KEY": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_SECRET_ACCESS_KEY", None
            ),
            "RCLONE_CONFIG_MYREMOTE_REGION": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_REGION", "us-east-1"
            ),
            "RCLONE_CONFIG_MYREMOTE_ACL": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_ACL", "private"
            ),
        }
    elif scheme == "azure" or scheme == "az":
        env = {
            "RCLONE_CONFIG_MYREMOTE_TYPE": "azureblob",
            "RCLONE_CONFIG_MYREMOTE_ACCOUNT": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_ACCOUNT", None
            ),
            "RCLONE_CONFIG_MYREMOTE_KEY": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_KEY", None
            ),
        }
    elif scheme == "oss":
        env = {
            "RCLONE_CONFIG_MYREMOTE_TYPE": "s3",
            "RCLONE_CONFIG_MYREMOTE_PROVIDER": "Alibaba",
            "RCLONE_CONFIG_MYREMOTE_ACCESS_KEY_ID": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_ACCESS_KEY_ID", None
            ),
            "RCLONE_CONFIG_MYREMOTE_SECRET_ACCESS_KEY": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_SECRET_ACCESS_KEY", None
            ),
            "RCLONE_CONFIG_MYREMOTE_ENDPOINT": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_ENDPOINT", "oss-cn-hongkong.aliyuncs.com"
            ),
            "RCLONE_CONFIG_MYREMOTE_ACL": os.environ.get(
                "RCLONE_CONFIG_MYREMOTE_ACL", "private"
            ),
        }
    return env


def parse_config_to_conn_str(config):
    if not config:
        return None

    if isinstance(config, str):
        try:
            config = json.loads(config)
        except json.JSONDecodeError:
            logger.error("The configuration is not a valid JSON string.")
            return None

    if not isinstance(config, dict):
        logger.error("The configuration is not a valid JSON string.")
        return None

    conn_type = config.pop("type", None)
    if conn_type is None:
        logger.error("The 'type' key is required in the configuration.")
        return None

    parts = [f"{key}={value}" for key, value in config.items()]
    connection_string = f":{conn_type}," + ",".join(parts) + ":"
    return connection_string
