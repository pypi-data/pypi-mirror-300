import pandas as pd
from model.balance_sheet_module.utils.main_general_setting import MainGeneralSetting
from model.utils.connect_to_cloud import GoogleCloudConnection
import scipy.stats
from copy import deepcopy
import numpy as np
from model.balance_sheet_module.utils.indeterminate_forms import (
    IndeterminateFormsMapOutput,
)
from typing import Dict
from model.utils.percentiles import PercentileEngine, InterpolationType
from model.utils.multicollinearity import Multicollinearity


def main(
    main_general_setting: MainGeneralSetting,
    long_list: pd.DataFrame,
    perim: pd.DataFrame,
    fl_intra_area: bool = True,
    fl_save_on_big_query: bool = False,
    overwrite_on_bigquery: bool = False,
) -> pd.DataFrame:
    # Set param based on the flag
    is_in_short_list_type = "after_corr_intra" if fl_intra_area else "after_corr_cross"
    destination_table = (
        main_general_setting.big_query_long_list_post_corr_intra_table
        if fl_intra_area
        else main_general_setting.big_query_long_list_post_corr_cross_table
    )
    # Select mln variable
    neg_mln = (
        IndeterminateFormsMapOutput.V_N_100000000
        if IndeterminateFormsMapOutput.V_N_100000000
        in main_general_setting.list_indeterminate_forms
        else IndeterminateFormsMapOutput.V_N_1000000
    )
    pos_mln = (
        IndeterminateFormsMapOutput.V_P_100000000
        if IndeterminateFormsMapOutput.V_P_100000000
        in main_general_setting.list_indeterminate_forms
        else IndeterminateFormsMapOutput.V_P_1000000
    )

    # Select univariate perimeter to consider
    perim_adj = deepcopy(perim)
    if fl_intra_area:
        long_list_filt = long_list[(long_list.is_in_short_list == True)].reset_index(
            drop=True
        )
    else:
        long_list_filt = long_list[
            (long_list.is_in_short_list_after_corr_intra == True)
        ].reset_index(drop=True)

    # ---------------------------------------------------------- #
    # 1) Manage indeterminate forms/+-mln
    # ---------------------------------------------------------- #
    for ind in range(long_list_filt.shape[0]):
        ind = long_list_filt.loc[ind, "name"]
        perim_adj[ind] = np.where(
            (perim_adj[ind] == neg_mln)
            | (perim_adj[ind] == pos_mln)
            | (perim_adj[ind] == IndeterminateFormsMapOutput.V_99999999.value),
            np.nan,
            perim_adj[ind],
        )
        name_perc = PercentileEngine(
            interpolation_type=InterpolationType.GE_THRESHOLD
        ).compute_percentile(perim_adj[ind].to_numpy(), percentile=[0.05, 0.95])
        perim_adj[ind] = np.where(
            perim_adj[ind] >= name_perc[0.95], name_perc[0.95], perim_adj[ind]
        )
        perim_adj[ind] = np.where(
            perim_adj[ind] <= name_perc[0.05], name_perc[0.05], perim_adj[ind]
        )

    # Create output dict
    short_list = []
    out_df = pd.DataFrame(
        {
            "indicator_left": [None],
            "indicator_right": [None],
            "area": [None],
            "ar_left": [None],
            "ar_right": [None],
            "missing_left": [None],
            "missing_right": [None],
            "zeros_left": [None],
            "zeros_right": [None],
            "indet_forms_left": [None],
            "indet_forms_right": [None],
            "correlation": None,
        }
    )
    # ---------------------------------------------------------- #
    # 2) compute pairwise correlation
    # ---------------------------------------------------------- #
    for ind1 in range(long_list_filt.shape[0]):
        name1 = long_list_filt.loc[ind1, "name"]
        for ind2 in range(long_list_filt.shape[0]):
            name2 = long_list_filt.loc[ind2, "name"]

            # Couples of indicators to be considered
            if name1 == name2:
                continue
            if fl_intra_area:
                if long_list_filt.loc[ind1, "area"] != long_list_filt.loc[ind2, "area"]:
                    continue

            # Compute correlation
            x = perim_adj[[name1, name2]]
            x_no_missing = x[
                ((x[name1].isnull() == False) & (x[name2].isnull() == False))
            ]
            corr = scipy.stats.pearsonr(
                x_no_missing[name1], x_no_missing[name2]
            ).statistic
            out = pd.DataFrame(
                {
                    "indicator_left": [name1],
                    "indicator_right": [name2],
                    "area": [long_list_filt.loc[ind1, "area"]],
                    "ar_left": [long_list_filt.loc[ind1, "accuracy_adj_sign"]],
                    "ar_right": [long_list_filt.loc[ind2, "accuracy_adj_sign"]],
                    "missing_left": [
                        x[(x[name1].isnull() == True)].shape[0] / x.shape[0]
                    ],
                    "missing_right": [
                        x[(x[name2].isnull() == True)].shape[0] / x.shape[0]
                    ],
                    "zeros_left": [long_list_filt.loc[ind1, "perc_zeros"]],
                    "zeros_right": [long_list_filt.loc[ind2, "perc_zeros"]],
                    "indet_forms_left": [long_list_filt.loc[ind1, "perc_indet_forms"]],
                    "indet_forms_right": [long_list_filt.loc[ind2, "perc_indet_forms"]],
                    "correlation": [corr],
                }
            )
            out_df = pd.concat([out_df, out], axis=0)
    out_df.reset_index(drop=True, inplace=True)
    if out_df.loc[0, "indicator_left"] == None:
        out_df = out_df.iloc[1:, :]

    # ---------------------------------------------------------- #
    # 3.1) Apply criteria in order to define winners and losers
    # ---------------------------------------------------------- #
    # Study only couples with correlation greater than correlation_threshold
    out_df_filtered = out_df[
        (abs(out_df.correlation) > main_general_setting.correlation_threshold)
    ]
    # Add variables with correlations greater than correlation_threshold
    list_ind_corr_gt_threshold = list(
        set(
            out_df_filtered["indicator_left"].to_list()
            + out_df_filtered["indicator_right"].to_list()
        )
    )
    short_list += [
        i for i in long_list_filt.name.to_list() if i not in list_ind_corr_gt_threshold
    ]

    # AR condition
    out_df_filtered["cond_ar_1"] = (
        abs(out_df_filtered["ar_left"] - out_df_filtered["ar_right"])
        > main_general_setting.correlation_threshold_accuracy
    )
    out_df_filtered["cond_ar_2"] = (
        out_df_filtered["ar_left"] - out_df_filtered["ar_right"]
        > main_general_setting.correlation_threshold_accuracy
    )

    # Missing condition
    out_df_filtered["cond_missing_1"] = (
        abs(out_df_filtered["missing_left"] - out_df_filtered["missing_right"]) > 0.0
    )
    out_df_filtered["cond_missing_2"] = (
        out_df_filtered["missing_left"] < out_df_filtered["missing_right"]
    )

    # Zeros condition
    out_df_filtered["cond_zeros_1"] = (
        abs(out_df_filtered["zeros_left"] - out_df_filtered["zeros_right"]) > 0.0
    )
    out_df_filtered["cond_zeros_2"] = (
        out_df_filtered["zeros_left"] < out_df_filtered["zeros_right"]
    )

    # Indeterminate forms condition
    out_df_filtered["cond_indet_forms_1"] = (
        abs(out_df_filtered["indet_forms_left"] - out_df_filtered["indet_forms_right"])
        > 0.0
    )
    out_df_filtered["cond_indet_forms_2"] = (
        out_df_filtered["indet_forms_left"] < out_df_filtered["indet_forms_right"]
    )

    # Apply conditions
    out_df_filtered["win_left"] = None
    out_df_filtered["win_left"] = np.where(
        out_df_filtered["cond_indet_forms_1"],
        out_df_filtered["cond_indet_forms_2"],
        out_df_filtered["win_left"],
    )
    out_df_filtered["win_left"] = np.where(
        out_df_filtered["cond_zeros_1"],
        out_df_filtered["cond_zeros_2"],
        out_df_filtered["win_left"],
    )
    out_df_filtered["win_left"] = np.where(
        out_df_filtered["cond_missing_1"],
        out_df_filtered["cond_missing_2"],
        out_df_filtered["win_left"],
    )
    out_df_filtered["win_left"] = np.where(
        out_df_filtered["cond_ar_1"],
        out_df_filtered["cond_ar_2"],
        out_df_filtered["win_left"],
    )
    out_df_filtered["loss_left"] = np.where(
        out_df_filtered["win_left"],
        False,
        True,
    )

    n_win_loss = (
        (
            out_df_filtered[["indicator_left", "win_left", "loss_left"]]
            .groupby(by="indicator_left")
            .agg({"win_left": "sum", "loss_left": "sum"})
        )
        .reset_index()
        .rename(columns={"win_left": "n_win", "loss_left": "n_loss"})
    )
    out_df_filtered = pd.merge(
        out_df_filtered, n_win_loss, how="left", on=["indicator_left"]
    )

    # ---------------------------------------------------------- #
    # 3.2) Create clusters of comparable variables
    # ---------------------------------------------------------- #
    ind_correlated = out_df_filtered.loc[
        (abs(out_df_filtered.correlation) > main_general_setting.correlation_threshold),
        ["indicator_left", "indicator_right"],
    ]
    clusters_comparables = dict()
    for ind in ind_correlated["indicator_left"].drop_duplicates().to_list():
        comparables = [ind]
        comparables = (
            ind_correlated.loc[
                (ind_correlated.indicator_left == ind),
                "indicator_right",
            ]
            .drop_duplicates()
            .to_list()
        )
        clusters_comparables[ind] = comparables
        additional_comparables = comparables
        while len(additional_comparables) > 0:
            x_tot = []
            for c in additional_comparables:
                x = (
                    ind_correlated.loc[
                        (out_df_filtered.indicator_left == c),
                        "indicator_right",
                    ]
                    .drop_duplicates()
                    .to_list()
                )
                x = [i for i in x if i not in clusters_comparables[ind]]
                x = [i for i in x if i not in x_tot]
                if len(x) > 0:
                    x_tot += x
            additional_comparables = x_tot
            if len(x_tot) > 0:
                clusters_comparables[ind] += x_tot
    clusters_comparables = {k: sorted(v) for k, v in clusters_comparables.items()}
    clusters_comparables_final = {}
    index_ = len(clusters_comparables)
    i = 0
    for k, v in clusters_comparables.items():
        if v not in clusters_comparables_final.values():
            clusters_comparables_final[i] = v
            i += 1

    # ---------------------------------------------------------- #
    # 4) Selection criteria
    # ---------------------------------------------------------- #
    out_df_wins = out_df_filtered[(out_df_filtered.n_win > out_df_filtered.n_loss)]

    # Compute VIF
    multic_df = pd.DataFrame()
    if fl_intra_area:
        ind_vif = {
            i: list(
                set(
                    out_df_wins.loc[(out_df_wins.area == i), "indicator_left"].to_list()
                    + out_df_wins.loc[
                        (out_df_wins.area == i), "indicator_right"
                    ].to_list()
                )
            )
            for i in out_df_wins.area.drop_duplicates().to_list()
        }
        for k, v in ind_vif.items():
            multic_df = pd.concat(
                [
                    multic_df,
                    Multicollinearity().compute_vif(ind_df=perim_adj, col=v),
                ],
                axis=0,
            )
    else:
        ind_vif = list(
            set(
                out_df_wins["indicator_left"].to_list()
                + out_df_wins["indicator_right"].to_list()
            )
        )
        multic_df = pd.concat(
            [
                multic_df,
                Multicollinearity().compute_vif(ind_df=perim_adj, col=ind_vif),
            ],
            axis=0,
        )
    multic_df.reset_index(drop=True, inplace=True)
    out_df_wins = pd.merge(
        out_df_wins,
        multic_df,
        how="left",
        left_on="indicator_left",
        right_on="indicator",
    ).drop(columns="indicator")

    # Add to the short list the variables with a level of multicollinearity lower/equal than 5
    out_df_wins_not_multicol = out_df_wins[
        (out_df_wins.vif <= main_general_setting.multicollinearity_threshold)
    ]
    short_list += out_df_wins_not_multicol["indicator_left"].drop_duplicates().to_list()

    # Cluster analysis
    out_df_wins_multicol = out_df_wins[
        (out_df_wins.vif > main_general_setting.multicollinearity_threshold)
    ]
    out_df_wins_multicol = (
        out_df_wins_multicol[["indicator_left", "ar_left", "n_win", "n_loss"]]
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={"indicator_left": "name", "ar_left": "ar"})
    )
    out_df_wins_multicol["ratio_win_loss"] = [
        1.0
        if out_df_wins_multicol.loc[i, "n_loss"] == 0.0
        else out_df_wins_multicol.loc[i, "n_win"]
        / out_df_wins_multicol.loc[i, "n_loss"]
        for i in range(out_df_wins_multicol.shape[0])
    ]
    out_df_wins_multicol["cluster"] = None
    for index_ in range(out_df_wins_multicol.shape[0]):
        out_df_wins_multicol.loc[index_, "cluster"] = [
            i
            for i, v in clusters_comparables_final.items()
            if out_df_wins_multicol.loc[index_, "name"] in v
        ][0]
    for index_ in out_df_wins_multicol.cluster.drop_duplicates().to_list():
        perim_index = out_df_wins_multicol[(out_df_wins_multicol.cluster == index_)]
        no_losses = perim_index[(perim_index.n_loss == 0)]
        max_win_ratio = perim_index[
            (perim_index.ratio_win_loss == perim_index.ratio_win_loss.max())
        ]
        max_ar = perim_index[(perim_index.ar == perim_index.ar.max())]
        if no_losses.shape[0] == 1:
            short_list.append(no_losses.name.to_list()[0])
        elif max_win_ratio.shape[0] == 1:
            short_list.append(max_win_ratio.name.to_list()[0])
        elif max_ar.shape[0] == 1:
            short_list.append(max_ar.name.to_list()[0])
        else:
            raise Exception(
                "Multicollinearity criteria must be checked - still multiple variables remaining"
            )

    # Merge the final short list to the overall indicator dataset
    final_long_list = pd.merge(
        long_list,
        pd.DataFrame(
            {
                "name": short_list,
                "is_in_short_list_"
                + is_in_short_list_type: [1 for i in range(len(short_list))],
            }
        ),
        how="left",
        on="name",
    )
    final_long_list["is_in_short_list_" + is_in_short_list_type] = np.where(
        final_long_list["is_in_short_list_" + is_in_short_list_type].isnull() == True,
        False,
        True,
    )
    if fl_save_on_big_query:
        GoogleCloudConnection(project=main_general_setting.project).upload_to_big_query(
            df=final_long_list,
            destination_table=destination_table,
            dataset=main_general_setting.big_query_dataset,
            overwrite=overwrite_on_bigquery,
        )

    return final_long_list


def download(
    main_general_setting: MainGeneralSetting, fl_intra_area: bool
) -> pd.DataFrame:
    if fl_intra_area:
        query_download_long_list = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_long_list_post_corr_intra_table}`"""
    else:
        query_download_long_list = f"""SELECT * FROM `{main_general_setting.project}.{main_general_setting.big_query_dataset}.{main_general_setting.big_query_long_list_post_corr_cross_table}`"""
    return GoogleCloudConnection(
        project=main_general_setting.project
    ).import_from_big_query(query=query_download_long_list)
