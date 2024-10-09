from model.utils.connect_to_cloud import GoogleCloudConnection
from model.balance_sheet_module.utils.univariate_analysis import UnivariateEngine
import os

import pandas as pd
from copy import deepcopy
from typing import Tuple, Dict
from model.balance_sheet_module.utils.main_general_setting import MainGeneralSetting


def main(
    main_general_setting: MainGeneralSetting,
    univ_dict: Dict[str, pd.DataFrame],
    long_list: pd.DataFrame,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> Dict[str, pd.DataFrame]:
    long_list_univ = dict()
    for k, v in univ_dict.items():
        long_list_univ[k] = UnivariateEngine().univ_stat(
            ind_df=v,
            long_list=long_list,
            list_indeterminate_forms=main_general_setting.list_indeterminate_forms,
        )

    if fl_save_on_big_query:
        for k, v in long_list_univ.items():
            GoogleCloudConnection(
                project=main_general_setting.project
            ).upload_to_big_query(
                df=v,
                destination_table=main_general_setting.univ_long_list_table + k.upper(),
                dataset=main_general_setting.big_query_dataset,
                overwrite=overwrite_on_bigquery,
            )
    return long_list_univ


def download(
    main_general_setting: MainGeneralSetting,
) -> Dict[str, pd.DataFrame]:
    long_list_univ = dict()
    for k in main_general_setting.univ_list_analysis:
        query = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.univ_long_list_table}{k.upper()}`"""
        long_list_univ[k] = GoogleCloudConnection(
            project=main_general_setting.project
        ).import_from_big_query(query=query)
    return long_list_univ


def create_report(
    main_general_setting: MainGeneralSetting,
    univ_long_list_dict: Dict[str, pd.DataFrame],
    univ_perim_dict: Dict[str, pd.DataFrame],
    fl_save_report: bool = False,
    direction_col: str = "direction_after_u_shape_treatment",
) -> None:
    for k, v in univ_perim_dict.items():
        if k in univ_long_list_dict.keys():
            UnivariateEngine().univariate_report(
                path=main_general_setting.univ_report_path,
                ind_df=v,
                long_list=univ_long_list_dict[k],
                analysis_name=k,
                fl_save=fl_save_report,
                direction_col=direction_col,
            )
