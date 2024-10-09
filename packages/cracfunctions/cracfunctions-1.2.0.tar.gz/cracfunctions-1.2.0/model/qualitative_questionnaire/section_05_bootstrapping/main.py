from model.utils.connect_to_cloud import GoogleCloudConnection
from model.qualitative_questionnaire.utils.main_general_setting import (
    MainGeneralSetting,
)
import pandas as pd
import numpy as np
from model.utils.bootstrapping import bootstrapping
from typing import Tuple
from copy import deepcopy


def main(
    main_general_setting: MainGeneralSetting,
    model: pd.DataFrame,
    perim: pd.DataFrame,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> Tuple[pd.DataFrame]:
    avg_beta = bootstrapping(
        df=perim,
        df_group=perim,
        model=model,
        var_group=main_general_setting.bootstrapping_grouping_variables,
        target_col="default",
        target_percentage=main_general_setting.bootstrapping_target_percentage,
        n_iter=main_general_setting.bootstrapping_n_iter,
        seed=main_general_setting.bootstrapping_seed,
    )
    # Compute scores
    perim_processed = deepcopy(perim)
    perim_processed["final_score"] = avg_beta.loc[
        (avg_beta.parameter == "intercept"), "beta"
    ].values[0]
    for var in avg_beta.loc[(avg_beta.parameter != "intercept"), "parameter"].to_list():
        perim_processed["final_score"] += (
            avg_beta.loc[(avg_beta.parameter == var), "beta"].values[0]
            * perim_processed[var]
        )
    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=avg_beta,
            destination_table=main_general_setting.bootstrapping_biquery_model_beta_out,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=perim_processed,
            destination_table=main_general_setting.bootstrapping_biquery_final_scores,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
    return avg_beta, perim_processed


def download(
    main_general_setting: MainGeneralSetting,
) -> Tuple[pd.DataFrame]:
    query_beta = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.bootstrapping_biquery_model_beta_out}`"""
    query_scores = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.bootstrapping_biquery_final_scores}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query_beta), GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(
        query=query_scores
    )
