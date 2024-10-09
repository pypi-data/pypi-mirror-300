from model.utils.connect_to_cloud import GoogleCloudConnection
import pandas as pd
from typing import List, Tuple
from copy import deepcopy

from model.balance_sheet_module.utils.main_general_setting import (
    MainGeneralSetting,
)
from model.balance_sheet_module.utils.indeterminate_forms import (
    IndeterminateFormsEngine,
)


def main(
    main_general_setting: MainGeneralSetting,
    indicator_df: pd.DataFrame,
    long_list: List,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    indicator_df_88_treatment = deepcopy(indicator_df)
    long_list_88_treatment = deepcopy(long_list)
    indet_engine = IndeterminateFormsEngine()
    long_list_88_treatment["substitution_param_88"] = None
    for i in range(len(main_general_setting.treatment_88_bucket)):
        long_list_88_treatment["n_bucket_88_" + str(i)] = None
    for ind in range(long_list_88_treatment.shape[0]):
        name = long_list_88_treatment.loc[ind, "name"]
        indicator_df_88_treatment.loc[:, name], param = indet_engine.v_88888888_treatment(
            ind_df=indicator_df_88_treatment,
            ind_col=name,
            buckets_bounds=main_general_setting.treatment_88_bucket,
            list_indet_forms=main_general_setting.list_indeterminate_forms,
        )
        long_list_88_treatment.loc[ind, "substitution_param_88"] = param.param
        for i in range(len(main_general_setting.treatment_88_bucket)):
            long_list_88_treatment.loc[
                ind, "n_bucket_88_" + str(i)
            ] = param.perc_bucket_pop[list(param.perc_bucket_pop.keys())[i]]

    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=indicator_df_88_treatment,
            destination_table=main_general_setting.big_query_88_treatment_table_name,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=long_list_88_treatment,
            destination_table=main_general_setting.big_query_long_list_after_88_table_name,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
    return indicator_df_88_treatment, long_list_88_treatment


def download(
    main_general_setting: MainGeneralSetting,
) -> Tuple[pd.DataFrame, pd.DataFrame]:

    query_download_perim_ind_88 = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_88_treatment_table_name}`"""
    query_download_long_list_88 = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_long_list_after_88_table_name}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query_download_perim_ind_88), GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(
        query=query_download_long_list_88
    )
