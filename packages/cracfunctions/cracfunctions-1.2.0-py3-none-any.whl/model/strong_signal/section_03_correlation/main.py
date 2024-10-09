import pandas as pd
from model.strong_signal.utils.main_general_setting import (
    MainGeneralSetting,
)
from model.utils.correlation_analysis_per_woe import main as main_corr
from model.utils.connect_to_cloud import GoogleCloudConnection
from copy import deepcopy
import scipy.stats
from typing import Tuple


def main(
    main_general_setting: MainGeneralSetting,
    perim: pd.DataFrame,
    univ_report: pd.DataFrame,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> Tuple[pd.DataFrame]:
    perim_processed = deepcopy(perim)
    univ_list = sorted(univ_report.indicator_name.drop_duplicates().to_list())
    univ_list_woe = [i + "_woe" for i in univ_list]
    correlation_matrix_pearson, correlation_matrix_spearman = main_corr(
        perim=perim_processed, var_list=univ_list_woe
    )
    correlation_matrix_pearson.reset_index(inplace=True)
    correlation_matrix_spearman.reset_index(inplace=True)

    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=correlation_matrix_pearson,
            destination_table=main_general_setting.big_query_corr_pearson_output_table,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=correlation_matrix_spearman,
            destination_table=main_general_setting.big_query_corr_spearman_output_table,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
    return correlation_matrix_pearson, correlation_matrix_spearman


def download(
    main_general_setting: MainGeneralSetting,
) -> pd.DataFrame:
    query_download_pearson = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_corr_pearson_output_table}`"""
    query_download_spearman = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_corr_spearman_output_table}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query_download_pearson), GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(
        query=query_download_spearman
    )
