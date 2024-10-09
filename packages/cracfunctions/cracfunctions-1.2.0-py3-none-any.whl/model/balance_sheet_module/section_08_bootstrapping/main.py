from model.utils.connect_to_cloud import GoogleCloudConnection
from model.balance_sheet_module.utils.main_general_setting import MainGeneralSetting
import pandas as pd
from copy import deepcopy
import numpy as np
from model.utils.combinatorial import CombinatorialEngine, ModelType
from model.utils.bootstrapping import bootstrapping


def main(
    main_general_setting: MainGeneralSetting,
    model: pd.DataFrame,
    perim: pd.DataFrame,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> pd.DataFrame:
    avg_beta = bootstrapping(
        df=perim,
        df_group=perim[(perim.fl_internal_default == 1)],
        model=model,
        var_group=main_general_setting.bootstrapping_grouping_variables,
        target_col="default",
        target_percentage=main_general_setting.bootstrapping_target_percentage,
        n_iter=main_general_setting.bootstrapping_n_iteration,
    )
    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=avg_beta,
            destination_table=main_general_setting.bootstrapping_biquery_model_beta_out,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
    return avg_beta


def download(
    main_general_setting: MainGeneralSetting,
) -> pd.DataFrame:
    query = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.bootstrapping_biquery_model_beta_out}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query)
