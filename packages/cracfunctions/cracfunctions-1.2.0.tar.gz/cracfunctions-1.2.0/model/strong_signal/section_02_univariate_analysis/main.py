import pandas as pd
from model.strong_signal.utils.main_general_setting import (
    MainGeneralSetting,
)
from model.utils.connect_to_cloud import GoogleCloudConnection
from model.utils.univariate_analysis_per_woe import (
    UnivariateEngine,
)
from copy import deepcopy
from typing import Tuple, Optional


def main(
    main_general_setting: MainGeneralSetting,
    perim: pd.DataFrame,
    ar_threshold: Optional[pd.DataFrame] = None,
    iv_threshold: Optional[pd.DataFrame] = None,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> pd.DataFrame:
    perim_processed = deepcopy(perim)
    univ_df, df_woe_add = UnivariateEngine().univ_stat(
        df=perim,
        ar_threshold=ar_threshold,
        iv_threshold=iv_threshold,
        treat_missing=main_general_setting.treat_missing_values,
        missing_map=main_general_setting.mapping_missing_values,
        ind_map=main_general_setting.ordering_map,
        woe_min_den_value=main_general_setting.woe_min_den_value,
    )

    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=univ_df,
            destination_table=main_general_setting.bigquery_table_univ_report,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=df_woe_add,
            destination_table=main_general_setting.bigquery_table_df_woe,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
    return univ_df, df_woe_add


def download(
    main_general_setting: MainGeneralSetting,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    query_download_report = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.bigquery_table_univ_report}`"""
    query_download_perim = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.bigquery_table_df_woe}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query_download_report), GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(
        query=query_download_perim
    )
