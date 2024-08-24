from os import getenv

from mini.exceptions import EnvinronmentVariableMissingError

STORAGE = getenv("GOOGLE_CLOUD_STORAGE_BUCKET")


def get_export_path(entity: str) -> str:
    if not STORAGE:
        raise EnvinronmentVariableMissingError(
            "GOOGLE_CLOUD_STORAGE_BUCKET is not set"
        )

    return f"gs://{STORAGE}/_tmp/{entity}/data-*.parquet"


def get_import_path(entity: str) -> str:
    if not STORAGE:
        raise EnvinronmentVariableMissingError(
            "GOOGLE_CLOUD_STORAGE_BUCKET is not set"
        )

    return f"gs://{STORAGE}/_tmp/{entity}"
