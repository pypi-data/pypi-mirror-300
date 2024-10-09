
import pandas as pd
from pydantic import BaseModel
from typing import Optional, Dict, Union, List
from enum import Enum
from pathlib import Path
import os


class DataRepositoryType(Enum):
    """Type of data repository type"""

    BIG_QUERY = ...
    CLOUD_STORAGE = ...


class GoogleCloudConnection:
    """Class designed for importing data from Google repositories"""

    BQ_STORAGE = ...

    def __init__(self, project: str) -> None:
        self._project = project

    @property
    def project(
        self,
    ) -> str:
        return self._project

    def _init_client(
        self, client_type: DataRepositoryType
    ) -> Union[pd.DataFrame, Dict]:
        """Initialize the proper Google data repository"""
        ...

    def import_from_big_query(
        self,
        query: str,
        return_query_job: bool = False,
        schema_model: Optional[BaseModel] = None,
    ) -> pd.DataFrame:
        """Execute a query on BigQuery and import the result inside a Python dataframe"""
        ...

    def import_from_cloud_storage(
        self,
        bucket_name: str,
        remote_directory: str,
        local_folder: Path,
        files_to_extract: Optional[List],
    ) -> Union[pd.DataFrame, Dict]:
        """Import folder/files from Cloud Storage to the local machine"""
        ...

    def upload_to_cloud_storage(
        self, local_path_file: Path, bucket_name: str, destination_blob_name: str
    ) -> None:
        ...

    def upload_to_big_query(
        self,
        df: pd.DataFrame,
        destination_table: str,
        dataset: Optional[str] = None,
        new_dataset: Optional[str] = None,
        overwrite: bool = False,
    ) -> None:
        ...

    def delete_bigquery_table(
        self,
        destination_table: str,
        dataset: Optional[str] = None,
    ) -> None:
        ...
