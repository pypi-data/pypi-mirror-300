import pandas as pd
from model.qualitative_questionnaire.utils.main_general_setting import (
    MainGeneralSetting,
)
from model.utils.connect_to_cloud import GoogleCloudConnection
from copy import deepcopy


def main(
    main_general_setting: MainGeneralSetting,
    perim: pd.DataFrame,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> pd.DataFrame:
    perim_processed = deepcopy(perim)
    for field, category in main_general_setting.ordering_map.items():
        perim_processed[field + "_num"] = perim_processed[field].apply(
            lambda x: category[x]
        )

    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=perim_processed,
            destination_table=main_general_setting.bigquery_table_perim_processed,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
    return perim_processed


def download(
    main_general_setting: MainGeneralSetting,
) -> pd.DataFrame:
    query_download_perim = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.bigquery_table_perim_processed}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query_download_perim)
