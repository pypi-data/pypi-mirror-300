import pandas as pd
from copy import deepcopy
from model.utils.bucket import BucketEngine
from typing import Optional
import numpy as np


def add_woe_to_perim(
    perim: pd.DataFrame,
    woe: pd.DataFrame,
    indicator_name_col: str = "variable",
    indicator_value_col: str = "value",
    woe_col: str = "woe",
) -> None:
    for ind in list(set(woe[indicator_name_col].to_list())):
        woe_dict = (
            woe[(woe[indicator_name_col] == ind)][[indicator_value_col, woe_col]]
            .set_index(indicator_value_col)[woe_col]
            .to_dict()
        )
        perim[ind + '_'+ woe_col] = perim[ind].replace(woe_dict)


def compute_score(
    perim_df: pd.DataFrame,
    beta_df: pd.DataFrame,
    score_col: str,
    parameter_col: str = "variable",
    beta_col: str = "coefficient"
) -> None:
    
    perim_df[score_col] = beta_df.loc[(beta_df[parameter_col] == "intercept"), beta_col].values[0]
    for ind in beta_df.loc[(beta_df[parameter_col] != "intercept"), parameter_col].to_list():
        perim_df[score_col] += round(perim_df[ind], 9) * round(
            beta_df.loc[(beta_df[parameter_col] == ind), beta_col].values[0], 9
        )
    perim_df[score_col] = perim_df[score_col].round(9)


def compute_score_with_areas(
    perim_df: pd.DataFrame,
    beta_df: pd.DataFrame,
    area_col: str = "area",
    total_area_col: str = "total",
    output_score : str = "qq"
) -> pd.DataFrame:

    score = deepcopy(perim_df)
    grouped_df = beta_df.groupby(area_col)
    all_area = [x for x in beta_df[area_col].unique().tolist() if x != total_area_col]

    for area in all_area:
        beta_df_area = grouped_df.get_group(area)
        compute_score(perim_df = score, beta_df = beta_df_area, score_col = "score_"+area.lower())

    beta_df_area_tot = grouped_df.get_group(total_area_col)
    compute_score(perim_df = score, beta_df = beta_df_area_tot, score_col = "score_"+output_score.lower())

    return score 


def apply_notch(
    perim_df: pd.DataFrame,
    bucket: pd.DataFrame,
    condition: str,
    notch: Optional[int] = None,
    specific_cluster: Optional[int] = None,
    cluster : str = "cluster_model",
    cluster_post_notch: str = "cluster_post_notch",
    is_specific_cluster = False,
)->pd.DataFrame:
        perim_mod = perim_df[condition]
        perim_non_mod = perim_df[~condition]
        if is_specific_cluster:
            perim_mod[cluster_post_notch] = specific_cluster
        else:
            perim_mod[cluster_post_notch] = perim_mod[cluster].astype(int) + notch
            perim_mod[cluster_post_notch] = perim_mod[cluster_post_notch].clip(upper=bucket["cluster_model"].max())
 
        perim_non_mod[cluster_post_notch] = perim_non_mod[cluster]
        return pd.concat([perim_mod, perim_non_mod],axis=0)


        # score["score_" + area] = df_area.loc[
        #     (df_area[parameter_col] == "intercept"), beta_col
        # ].values[0]
        # for ind in df_area.loc[
        #     (df_area[parameter_col] != "intercept"), parameter_col
        # ].to_list():
        #     score["score_" + area] += round(score[ind], 9) * round(
        #         beta.loc[(beta[parameter_col] == ind), beta_col].values[0], 9
        #     )
        # score["score_" + area] = score["score_" + area].round(9)



            # score["total_score"] = df_area.loc[
    #     (df_area[parameter_col] == "intercept"), beta_col
    # ].values[0]
    # for ind in df_area.loc[
    #     (df_area[parameter_col] != "intercept"), parameter_col
    # ].to_list():
    #     score["total_score"] += round(score["score_" + ind], 9) * round(
    #         beta.loc[(beta[parameter_col] == ind), beta_col].values[0], 9
    #     )
    # score["total_score"] = score["total_score"].round(9)


def apply_cap (
perim_df : pd.DataFrame,
cap : int,
cluster : str = "score_model",
flag : Optional[int] = 0,
flag_col : Optional[str] = None,
flag_cap : Optional[int] = 0,
)->pd.DataFrame:
    if flag == 0:
        perim_df[cluster+"_post_cap"] = np.where(perim_df[cluster].astype(int) <= cap, cap, perim_df[cluster].astype(int))
    if flag == 1:
        perim_df[cluster+"_post_cap"] = np.where((perim_df[cluster] < cap) & (perim_df[flag_col].isna()), cap, 
        np.where((perim_df[cluster] <cap) & (pd.notna(perim_df[flag_col])), flag_cap, perim_df[cluster]))


    return perim_df