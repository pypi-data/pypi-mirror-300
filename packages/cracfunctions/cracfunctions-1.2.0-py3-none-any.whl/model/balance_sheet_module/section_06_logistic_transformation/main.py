from model.utils.connect_to_cloud import GoogleCloudConnection
from model.balance_sheet_module.utils.main_general_setting import MainGeneralSetting
from model.utils.regression_model import LogisticEngine, LogisticParameter
import pandas as pd
from copy import deepcopy
from typing import Tuple


def main(
    main_general_setting: MainGeneralSetting,
    long_list: pd.DataFrame,
    perim: pd.DataFrame,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> pd.DataFrame:
    perim_adj = deepcopy(perim)
    long_list_adj = deepcopy(long_list)
    long_list_adj["logistic_t_center"] = None
    long_list_adj["logistic_t_slope"] = None
    long_list_adj["logistic_t_mean"] = None
    long_list_adj["logistic_t_stdev"] = None
    for ind in long_list.name.to_list():
        # Adjust sign: all the variable are set with direction equals to 1
        # Applying the logistic then will change the sign again
        if (
            long_list_adj.loc[
                (long_list_adj.name == ind), "direction_after_u_shape_treatment"
            ].values[0]
            == -1
        ):
            perim_adj[ind] *= -1
        perim_adj[ind], log_param = LogisticEngine(
            cutoff_multiplier=main_general_setting.logistic_t_cutoff_multiplier,
            slope_num=main_general_setting.logistic_t_slope_num,
        ).estimate_apply_logistic_transformation(ind_df=perim_adj, ind_col=ind)
        long_list_adj.loc[(long_list_adj.name == ind), "logistic_t_center"] = log_param[
            LogisticParameter.CENTER
        ]
        long_list_adj.loc[(long_list_adj.name == ind), "logistic_t_slope"] = log_param[
            LogisticParameter.SLOPE
        ]
        long_list_adj.loc[(long_list_adj.name == ind), "logistic_t_mean"] = log_param[
            LogisticParameter.MEAN
        ]
        long_list_adj.loc[(long_list_adj.name == ind), "logistic_t_stdev"] = log_param[
            LogisticParameter.STDEV
        ]

    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=perim_adj,
            destination_table=main_general_setting.logistic_t_big_query_perim,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=long_list_adj,
            destination_table=main_general_setting.logistic_t_big_query_long_list,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )

    return perim_adj, long_list_adj


def download(
    main_general_setting: MainGeneralSetting,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    query_download_perim = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.logistic_t_big_query_perim}`"""
    query_download_long_list = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.logistic_t_big_query_long_list}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query_download_perim), GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(
        query=query_download_long_list
    )
