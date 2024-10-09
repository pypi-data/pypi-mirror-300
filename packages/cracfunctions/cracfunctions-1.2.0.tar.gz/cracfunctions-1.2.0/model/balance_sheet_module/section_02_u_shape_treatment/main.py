from model.utils.connect_to_cloud import GoogleCloudConnection
import pandas as pd
from typing import List, Tuple, Dict
from model.balance_sheet_module.utils.u_shape import UShapeType
from model.balance_sheet_module.utils.u_shape import UShapeEngine
from model.balance_sheet_module.utils.main_general_setting import (
    MainGeneralSetting,
)
from copy import deepcopy


def main(
    main_general_setting: MainGeneralSetting,
    indicator_df: pd.DataFrame,
    long_list: pd.DataFrame,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    indicator_df_u_shape = deepcopy(indicator_df)
    long_list_u_shape = deepcopy(long_list)
    long_list_u_shape["is_u_shape"] = None
    long_list_u_shape["direction_after_u_shape_treatment"] = None
    long_list_u_shape["ushape_percentile_perc"] = None
    long_list_u_shape["ushape_percentile_value"] = None
    ushape_engine = UShapeEngine(
        buckets_bounds=main_general_setting.u_shape_treatment_bucket
    )
    for ind in range(long_list_u_shape.shape[0]):
        name = long_list_u_shape.loc[ind, "name"]
        ushape_type = ushape_engine.identify(
            ind_perim=indicator_df_u_shape,
            ind_col=name,
        )
        if ushape_type == UShapeType.NO_USHAPE:
            long_list_u_shape.loc[ind, "is_u_shape"] = False
            long_list_u_shape.loc[
                ind, "direction_after_u_shape_treatment"
            ] = long_list_u_shape.loc[ind, "direction"]
        else:
            if ushape_type == UShapeType.USHAPE_UP:
                long_list_u_shape.loc[ind, "direction_after_u_shape_treatment"] = -1
            else:
                long_list_u_shape.loc[ind, "direction_after_u_shape_treatment"] = 1
            long_list_u_shape.loc[ind, "is_u_shape"] = True
            (
                ind_transformed,
                param,
            ) = ushape_engine.estimate_apply_quadratic_transformation(
                ind_df=indicator_df_u_shape,
                indicator_name=name,
                direction=long_list_u_shape.loc[
                    ind, "direction_after_u_shape_treatment"
                ],
                list_indet_forms=main_general_setting.list_indeterminate_forms,
            )
            indicator_df_u_shape.loc[:, name] = ind_transformed
            long_list_u_shape.loc[ind, "ushape_percentile_perc"] = param.percentile_perc
            long_list_u_shape.loc[
                ind, "ushape_percentile_value"
            ] = param.percentile_value

    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=indicator_df_u_shape,
            destination_table=main_general_setting.big_query_ushape_table_name,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=long_list_u_shape,
            destination_table=main_general_setting.big_query_long_list_after_ushape_table_name,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
    return indicator_df_u_shape, long_list_u_shape


def download(
    main_general_setting: MainGeneralSetting,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    query_download_perim_ind_ushape = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_ushape_table_name}`"""
    query_download_long_list_ushape = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_long_list_after_ushape_table_name}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(
        query=query_download_perim_ind_ushape
    ), GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(
        query=query_download_long_list_ushape
    )
