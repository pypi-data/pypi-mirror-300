from google.cloud import bigquery, storage, bigquery_storage
import pandas as pd
from pydantic import BaseModel
from typing import Optional, Dict, Union, List
from enum import Enum
from pathlib import Path
import os


class DataRepositoryType(Enum):
    """Type of data repository type"""

    BIG_QUERY = bigquery
    CLOUD_STORAGE = storage


class GoogleCloudConnection:
    """Class designed for importing data from Google repositories"""

    BQ_STORAGE = bigquery_storage.BigQueryReadClient()

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
        return client_type.value.Client(project=self._project)

    def execute_on_big_query(
        self,
        query: str,
    ) -> None:
        """Execute a query on BigQuery"""
        query_job = self._init_client(client_type=DataRepositoryType.BIG_QUERY).query(
            query
        )
        # Wait for the query to finish
        results = query_job.result()

        # Job stat
        print(f"Query job ID: {query_job.job_id}")
        print(f"Query state: {query_job.state}")
        print(f"Bytes processed: {query_job.total_bytes_processed}")
        print(f"Query was cached: {query_job.cache_hit}")
        print(f"Execution time: {query_job.ended - query_job.started}")

    def import_from_big_query(
        self,
        query: str,
        return_query_job: bool = False,
        schema_model: Optional[BaseModel] = None,
    ) -> pd.DataFrame:
        """Execute a query on BigQuery and import the result"""
        query_job = self._init_client(client_type=DataRepositoryType.BIG_QUERY).query(
            query
        )
        if return_query_job:
            return query_job
        if schema_model:
            ...
        return query_job.to_dataframe(bqstorage_client=self.BQ_STORAGE)

    def import_from_cloud_storage(
        self,
        bucket_name: str,
        remote_directory: str,
        local_folder: Path,
        files_to_extract: Optional[List],
    ) -> Union[pd.DataFrame, Dict]:
        """Import folder/files from Cloud Storage to the local machine"""
        blobs = self._init_client(
            client_type=DataRepositoryType.CLOUD_STORAGE
        ).list_blobs(bucket_name, prefix=remote_directory)
        if not os.oath.exists(local_folder):
            os.makedirs(local_folder)
        for blob in blobs:
            if "." in blob.name:
                if files_to_extract:
                    if blob.name in files_to_extract:
                        local_file = local_folder.joinpath(blob.name)
                        blob.download_to_filename(local_file)

    def upload_to_cloud_storage(
        self, local_path_file: Path, bucket_name: str, destination_blob_name: str
    ) -> None:
        client = self._init_client(client_type=DataRepositoryType.CLOUD_STORAGE)
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_path_file)

    def upload_to_big_query(
        self,
        df: pd.DataFrame,
        dataset: str,
        destination_table: str,
        overwrite: bool = False,
    ) -> None:
        """
        df: pandas dataframe to upload
        destination_table: name of the table in bigquery
        dataset: dataset of bigquery in which the table must be saved
        overwrite: overwrite the existing table
        """
        client = self._init_client(client_type=DataRepositoryType.BIG_QUERY)
        if overwrite:
            job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        else:
            job_config = bigquery.LoadJobConfig()
        dataset = client.dataset(dataset)
        table_ref = dataset.table(destination_table)
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()
        print("Loaded dataframe to {}".format(table_ref.path))

    def delete_bigquery_table(
        self,
        destination_table: str,
        dataset: Optional[str] = None,
    ) -> None:
        if dataset:
            client = self._init_client(client_type=DataRepositoryType.BIG_QUERY)
            table_del = f"{self._project}.{dataset}.{destination_table}"
            user_answer = input(
                f"Are you sure you want to delete {table_del}? write yes if you want to delete the table. "
            )
            if user_answer.lower() == "yes":
                try:
                    client.delete_table(table_del)
                    print(f"{table_del} deleted")
                except:
                    print(f"{table_del} not found")
