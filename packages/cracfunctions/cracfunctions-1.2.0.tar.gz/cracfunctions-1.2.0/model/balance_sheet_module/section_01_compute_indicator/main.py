from model.utils.connect_to_cloud import GoogleCloudConnection
from model.balance_sheet_module.utils.indicator import (
    IndicatorCalcEngine,
    IndicatorType,
)
import pandas as pd
from copy import deepcopy
from model.balance_sheet_module.utils.indeterminate_forms import (
    IndeterminateForms,
    IndeterminateFormsMapOutput,
)
from model.balance_sheet_module.utils.main_general_setting import (
    MainGeneralSetting,
)
from typing import List, Dict, Tuple, Optional


def elab_indicator(
    perim: pd.DataFrame,
    long_list: pd.DataFrame,
    indicator_keys: List,
    list_indeterminate_forms: List[IndeterminateFormsMapOutput],
    ind_type_col: str = "Tipo",
) -> pd.DataFrame:
    """Given the perimeter and the long list, the function computes the indicators values.
    perim: perimeter
    long_list: long list
    indicator_keys: which columns to consider in the output dataset (in addition to the indicators)
    list_indeterminate_forms: list of indeterminate forms presents in the sample
    """
    indicator_df = perim[indicator_keys]
    for ind in range(long_list.shape[0]):
        indeterminate_forms_map = {
            IndeterminateForms.DN_NN: long_list.loc[ind, "DnNn"],
            IndeterminateForms.DN_NP: long_list.loc[ind, "DnNp"],
            IndeterminateForms.DN_N0: long_list.loc[ind, "DnN0"],
            IndeterminateForms.D0_NN: long_list.loc[ind, "D0Nn"],
            IndeterminateForms.D0_NP: long_list.loc[ind, "D0Np"],
            IndeterminateForms.D0_N0: long_list.loc[ind, "D0N0"],
            IndeterminateForms.DP_NN: long_list.loc[ind, "DpNn"],
            IndeterminateForms.DP_NP: long_list.loc[ind, "DpNp"],
            IndeterminateForms.DP_N0: long_list.loc[ind, "DpN0"],
        }
        ind_type = (
            IndicatorType.RATIO
            if long_list.loc[ind, ind_type_col] == "R"
            else (
                IndicatorType.LOG
                if long_list.loc[ind, ind_type_col] == "L"
                else IndicatorType.FITCH
            )
        )
        time_series_df = IndicatorCalcEngine(
            name=long_list.loc[ind, "name"],
            numerator_formula=long_list.loc[ind, "numerator"],
            denominator_formula=long_list.loc[ind, "denominator"],
            indicator_type=ind_type,
            keys=indicator_keys,
        ).compute_indicator_df(
            input_df=perim, indeterminate_forms_map=indeterminate_forms_map
        )

        indicator_df = pd.merge(
            left=indicator_df, right=time_series_df, how="left", on=indicator_keys
        )

    return indicator_df


def main(
    main_general_setting: MainGeneralSetting,
    perim: pd.DataFrame,
    long_list: pd.DataFrame,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
    name_bq_table_perim: Optional[str] = None,
) -> pd.DataFrame:
    indicator_df = elab_indicator(
        perim=perim,
        long_list=long_list,
        indicator_keys=main_general_setting.indicator_keys,
        list_indeterminate_forms=main_general_setting.list_indeterminate_forms,
    )
    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            indicator_df,
            destination_table=name_bq_table_perim,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
    return indicator_df


def download(
    main_general_setting: MainGeneralSetting,
) -> pd.DataFrame:
    query_download_perim_ind = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_indicator_table_name}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query_download_perim_ind)
