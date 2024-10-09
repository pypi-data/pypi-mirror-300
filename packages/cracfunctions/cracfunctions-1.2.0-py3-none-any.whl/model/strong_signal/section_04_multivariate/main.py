import pandas as pd
from model.strong_signal.utils.main_general_setting import (
    MainGeneralSetting,
)
from model.utils.connect_to_cloud import GoogleCloudConnection
from copy import deepcopy
import scipy.stats
from typing import Tuple, List, Dict
from model.utils.regression_model import LogisticEngine


def main(
    main_general_setting: MainGeneralSetting,
    perim: pd.DataFrame,
    var_list: List[str],
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    model_dict = {k: None for k in main_general_setting.area_ind.keys()}
    for k in model_dict.keys():
        stop_search_model = True
        var_test = main_general_setting.area_ind[k]
        while stop_search_model:
            model_out = LogisticEngine().fit(
                features=perim[var_test], target=perim["default"]
            )
            if (
                model_out.model_report[
                    (model_out.model_report.parameter != "intercept")
                ].shape[0]
                != model_out.model_report[
                    (
                        (model_out.model_report.parameter != "intercept")
                        & (
                            model_out.model_report.p_values
                            <= main_general_setting.multiv_pvalues_threshold
                        )
                    )
                ].shape[0]
            ):
                var_test = model_out.model_report.loc[
                    (
                        (model_out.model_report.parameter != "intercept")
                        & (
                            model_out.model_report.p_values
                            <= main_general_setting.multiv_pvalues_threshold
                        )
                    ),
                    "parameter",
                ].to_list()
            else:
                stop_search_model = False
                model_dict[k] = model_out
    model_scores = {
        k: LogisticEngine().create_scores(model=v.model) for k, v in model_dict.items()
    }
    model_scores_df = perim[
        main_general_setting.col_key
        + main_general_setting.bootstrapping_grouping_variables
        + ["default"]
    ]

    for k, v in model_scores.items():
        model_scores_df = pd.concat([model_scores_df, pd.DataFrame({k: v})], axis=1)
    model_dict["final"] = LogisticEngine().fit(
        features=model_scores_df[list(model_dict.keys())], target=perim["default"]
    )
    model_dict_final = {k: v.model_report for k, v in model_dict.items()}

    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=model_scores_df,
            destination_table=main_general_setting.big_query_multiv_scores,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )
        for k, v in model_dict_final.items():
            GoogleCloudConnection(
                project=main_general_setting.project
            ).upload_to_big_query(
                df=v,
                destination_table=main_general_setting.big_query_multiv_models + k,
                dataset=main_general_setting.big_query_dataset,
                overwrite=overwrite_on_bigquery,
            )
    return model_scores_df, model_dict_final


def download(
    main_general_setting: MainGeneralSetting,
) -> Tuple[pd.DataFrame, Dict[str, pd.DataFrame]]:
    # Download scores
    query_download_scores = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_multiv_scores}`"""
    scores = GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query_download_scores)

    # Download models
    dict_model = dict()
    for k in main_general_setting.area_ind.keys():
        query_download_model = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_multiv_models+k}`"""
        dict_model[k] = GoogleCloudConnection(
            project=main_general_setting.project
        ).import_from_big_query(query=query_download_model)
    query_download_final = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_multiv_models+"final"}`"""
    dict_model["final"] = GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query_download_final)
    return scores, dict_model
