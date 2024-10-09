import pandas as pd
from typing import List, Optional
import numpy as np
from model.utils.combinatorial import CombinatorialEngine, ModelType
from copy import deepcopy
from tqdm import tqdm


def bootstrapping(
    df: pd.DataFrame,
    df_group: pd.DataFrame,
    model: pd.DataFrame,
    var_group: List[str],
    target_col: str = "default",
    target_percentage: float = 0.25,
    n_iter: int = 100,
    seed: Optional[int] = None,
) -> pd.DataFrame:
    # Target N
    n_target_add = int(
        (target_percentage * df.shape[0] - df[target_col].sum())
        / (1 - target_percentage)
    )
    n_target_overall = n_target_add + df[target_col].sum()

    # -------------------------------------------------------------- #
    # Compute target percentages #
    # -------------------------------------------------------------- #
    # Percentages calculated on the grouping dataframe
    n_target_group = (
        df_group[var_group + [target_col]]
        .groupby(by=var_group)[target_col]
        .sum()
        .reset_index()
    )
    n_target_group[target_col + "_perc"] = (
        n_target_group[target_col] / n_target_group[target_col].sum()
    )
    n_target_group[target_col + "_target"] = (
        n_target_group[target_col + "_perc"] * n_target_overall
    )
    n_target_group[target_col + "_target_add"] = (
        n_target_group[target_col + "_target"] - n_target_group[target_col]
    )

    # Overall
    n_target_group_overall = (
        df[var_group + [target_col]]
        .groupby(by=var_group)[target_col]
        .sum()
        .reset_index()
        .rename(columns={target_col: target_col + "_asis"})
    )
    n_target_group_overall = pd.merge(
        n_target_group_overall,
        n_target_group,
        how="left",
        on=var_group,
    )
    n_target_group_overall[target_col + "_target_add"] = (
        n_target_group_overall[target_col + "_target"]
        - n_target_group_overall[target_col + "_asis"]
    )

    # -------------------------------------------------------------- #
    # Perform bootstrapping #
    # -------------------------------------------------------------- #
    # Set the seed
    if seed:
        np.random.seed(seed)

    model_bootstrapping = []
    df["var_group"] = ""
    n_target_group_overall["var_group"] = ""
    for v in var_group:
        df.var_group += "__" + df[v].astype(str)
        n_target_group_overall["var_group"] += "__" + n_target_group_overall[v].astype(
            str
        )
    for n_sim in tqdm(
        range(n_iter),
        desc="Bootstrapping: ",
        ascii=True,
    ):
        df_sim = deepcopy(df)
        for v_group in df["var_group"].drop_duplicates().to_list():
            perim_v = df[
                ((df.var_group == v_group) & (df[target_col] == 1))
            ].reset_index()
            n_extract = n_target_group_overall.loc[
                (n_target_group_overall.var_group == v_group),
                target_col + "_asis",
            ].values[0]
            pos_extract = np.random.choice(
                np.arange(n_extract),
                size=round(
                    n_target_group_overall.loc[
                        (n_target_group_overall.var_group == v_group),
                        target_col + "_target_add",
                    ].values[0]
                ),
                replace=True,
            )
            df_sim = pd.concat([df_sim, perim_v.iloc[pos_extract, :]])
        comb_engine = CombinatorialEngine(model=ModelType.LOGISTIC_REGRESSION)
        model_bootstrapping += comb_engine.create_models(
            ind_df=df_sim,
            target_var=target_col,
            model_list=[
                model.loc[(model.parameter != "intercept"), "parameter"].to_list()
            ],
        )

    # -------------------------------------------------------------- #
    # Compute average betas #
    # -------------------------------------------------------------- #

    model_mean = model_bootstrapping[0].model.params
    for index_mod in range(len(model_bootstrapping)):
        if index_mod == 0:
            continue
        model_mean += model_bootstrapping[index_mod].model.params

    model_mean = model_mean / len(model_bootstrapping)
    model_mean = (
        model_mean.to_frame("beta").reset_index().rename(columns={"index": "parameter"})
    )
    model_mean["parameter"] = np.where(
        model_mean.parameter == "const", "intercept", model_mean.parameter
    )
    return model_mean
