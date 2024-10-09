from model.utils.connect_to_cloud import GoogleCloudConnection
from model.qualitative_questionnaire.utils.main_general_setting import (
    MainGeneralSetting,
)
import pandas as pd
import numpy as np
from model.utils.bucket import BucketEngine
from copy import deepcopy
from typing import Tuple


def main(
    main_general_setting: MainGeneralSetting,
    perim: pd.DataFrame,
    model: pd.DataFrame,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> pd.DataFrame:
    score_bucket = BucketEngine(
        n_bucket=main_general_setting.n_bucket,
        score_unit_interval=main_general_setting.score_unit_interval,
        t_test_threshold=main_general_setting.t_test_threshold,
        hhi_map=main_general_setting.hhi_map,
    ).estimate_n_bucket(ind_df=perim, score_col="final_score")
    final_scores = ...
    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=score_bucket,
            destination_table=main_general_setting.big_query_bucket,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=final_scores,
            destination_table=main_general_setting.big_query_final_bucket_score,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
    return score_bucket


def download(
    main_general_setting: MainGeneralSetting,
) -> Tuple[pd.DataFrame]:
    query_bucket = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_bucket}`"""
    query_scores = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_final_bucket_score}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query_bucket), GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(
        query=query_scores
    )
