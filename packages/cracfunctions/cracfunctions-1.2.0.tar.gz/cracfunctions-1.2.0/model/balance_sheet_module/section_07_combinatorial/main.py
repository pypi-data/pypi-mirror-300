from model.utils.connect_to_cloud import GoogleCloudConnection
from model.balance_sheet_module.utils.main_general_setting import MainGeneralSetting
from model.utils.combinatorial import CombinatorialEngine, ModelType
import pandas as pd
from copy import deepcopy
from typing import Tuple
import warnings
from tqdm import tqdm
from model.utils.percentiles import PercentileEngine, InterpolationType


def main_initial_selection(
    main_general_setting: MainGeneralSetting,
    long_list: pd.DataFrame,
    perim: pd.DataFrame,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> pd.DataFrame:
    long_list_adj = deepcopy(long_list)
    long_list_adj = long_list_adj[
        (long_list_adj.is_in_short_list_after_corr_cross == True)
    ].reset_index(drop=True)
    long_list_adj_dict = {
        long_list_adj.loc[ind, "name"]: long_list_adj.loc[ind, "area"]
        for ind in range(long_list_adj.shape[0])
    }
    # ---------------------------------------------------------- #
    # Model creation
    # ---------------------------------------------------------- #
    comb_engine = CombinatorialEngine(
        model=ModelType.LOGISTIC_REGRESSION,
        min_n_variable=main_general_setting.combinatorial_min_n_variable,
        max_n_variable=main_general_setting.combinatorial_max_n_variable,
    )
    model_list = comb_engine.create_model_list(
        ind_df=perim, variables=long_list_adj_dict
    )
    len_int_batch = len(model_list) // main_general_setting.combinatorial_n_batch
    n_mod_key = 0
    for n_batch in tqdm(
        range(main_general_setting.combinatorial_n_batch + 1),
        desc="Batch status",
        ascii=True,
    ):
        model_list_filt = (
            model_list[n_batch * len_int_batch :]
            if n_batch == main_general_setting.combinatorial_n_batch
            else model_list[n_batch * len_int_batch : (n_batch + 1) * len_int_batch]
        )
        # Ignore warnings during the model fitting
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            models = comb_engine.create_models(
                ind_df=perim,
                target_var="default",
                model_list=model_list_filt,
                significance_level=main_general_setting.logistic_significance_level,
            )

        # ---------------------------------------------------------- #
        # Model selection: select only models with all the p-values
        # lower than the chosen threshold
        # ---------------------------------------------------------- #
        models_filt_1 = [
            mod.model_report
            for mod in models
            if mod.model_report[
                (
                    mod.model_report.p_values
                    > main_general_setting.combinatorial_criteria[
                        "combinatorial_coef_pvalue_threshold"
                    ]
                )
            ].shape[0]
            == 0
        ]
        if len(models_filt_1) == 0:
            continue
        models_filt_1_df = pd.DataFrame()
        for n_mod, i in enumerate(models_filt_1):
            i["model_id"] = n_mod + n_mod_key
            models_filt_1_df = pd.concat([models_filt_1_df, i], axis=0)
        models_filt_1_df["n_batch"] = n_batch
        models_filt_1_df.sort_values(by=["n_batch", "model_id"], inplace=True)
        n_mod_key += n_mod + 1
        if fl_save_on_big_query:
            GoogleCloudConnection(
                project=main_general_setting.project
            ).upload_to_big_query(
                df=models_filt_1_df,
                destination_table=main_general_setting.combinatorial_initial_models,
                dataset=main_general_setting.big_query_dataset,
                overwrite=overwrite_on_bigquery,
            )
        return models_filt_1_df


def download(
    main_general_setting: MainGeneralSetting,
) -> pd.DataFrame:
    query = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.combinatorial_initial_models}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query)
