import pandas as pd
from typing import Dict, Tuple, Optional
from model.utils.accuracy import AccuracyEngine
from model.utils.woe import WOEEngine
import numpy as np
from copy import deepcopy


class UnivariateEngine:
    @staticmethod
    def univ_stat(
        df: pd.DataFrame,
        ind_map: Dict,
        ar_threshold: Optional[pd.DataFrame] = None,
        iv_threshold: Optional[pd.DataFrame] = None,
        treat_missing: bool = False,
        missing_map: Optional[Dict[str, str]] = None,
        woe_min_den_value: float = 0.0,
        def_col: str = "default",
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        out = pd.DataFrame()
        woe_engine = WOEEngine(min_den_value=woe_min_den_value)
        df_proc_woe = deepcopy(df)
        for ind, ind_map in ind_map.items():
            df_stat = (
                (df[[ind, "cod_sndg"]].groupby(by=[ind]).agg({"cod_sndg": "count"}))
                .reset_index()
                .rename(
                    columns={
                        "cod_sndg": "n_obs",
                        ind: "indicator_value",
                    }
                )
            )
            df_stat = pd.concat(
                [
                    pd.DataFrame(
                        {"indicator_name": np.repeat(ind, int(df_stat.shape[0]))}
                    ),
                    df_stat,
                ],
                axis=1,
            )
            # Calcolo WOE
            df_woe = woe_engine.woe_calc(ind_df=df, ind_name=ind, def_col=def_col)
            df_stat = pd.merge(
                df_stat, df_woe, how="left", on=["indicator_name", "indicator_value"]
            )
            woe_dict_ind = {
                i: df_woe.loc[(df_woe.indicator_value == i), "woe"]
                .drop_duplicates()
                .to_list()[0]
                for i in df_woe.indicator_value.drop_duplicates().to_list()
            }
            df_proc_woe[ind + "_woe"] = df_proc_woe[ind].apply(
                lambda x: woe_dict_ind[x]
            )

            # Check Woe direction
            if treat_missing:
                if missing_map is not None:
                    missing_val = missing_map[ind]
                    woe_num_direction = list(
                        df_proc_woe.loc[
                            (df_proc_woe[ind] != missing_val),
                            [ind + "_num", ind + "_woe"],
                        ]
                        .drop_duplicates()
                        .reset_index()
                        .sort_values(by=ind + "_num")
                        .index
                    )
                    woe_direction = list(
                        df_proc_woe.loc[
                            (df_proc_woe[ind] != missing_val),
                            [ind + "_num", ind + "_woe"],
                        ]
                        .drop_duplicates()
                        .reset_index()
                        .sort_values(by=ind + "_woe")
                        .index
                    )
                else:
                    raise Exception(
                        "Provide a mapping table to recognize missing values"
                    )
            else:
                woe_num_direction = list(
                    df_proc_woe[[ind + "_num", ind + "_woe"]]
                    .drop_duplicates()
                    .reset_index()
                    .sort_values(by=ind + "_num")
                    .index
                )
                woe_direction = list(
                    df_proc_woe[[ind + "_num", ind + "_woe"]]
                    .drop_duplicates()
                    .reset_index()
                    .sort_values(by=ind + "_woe")
                    .index
                )
            df_stat["woe_direction_check"] = (
                "consistent"
                if (
                    woe_direction == woe_num_direction
                    or woe_direction == list(reversed(woe_num_direction))
                )
                else "not consistent"
            )
            # Calcolo DR/AR/IV
            df_stat["dr"] = df_stat["n_default"] / df_stat["n_obs"]
            if treat_missing:
                if missing_map is not None:
                    missing_val = missing_map[ind]
                    df_stat["ar"] = AccuracyEngine().compute_somersd(
                        x=df_proc_woe.loc[
                            (df_proc_woe[ind] != missing_val), ind + "_woe"
                        ].to_numpy(),
                        y=df_proc_woe.loc[
                            (df_proc_woe[ind] != missing_val), def_col
                        ].to_numpy(),
                    )
                else:
                    raise Exception(
                        "Provide a mapping table to recognize missing values"
                    )
            else:
                df_stat["ar"] = AccuracyEngine().compute_somersd(
                    x=df_proc_woe[ind + "_woe"].to_numpy(),
                    y=df_proc_woe[def_col].to_numpy(),
                )
            if ar_threshold is not None:
                df_stat["soglia_ar"] = [
                    ar_threshold.loc[
                        ((ar_threshold["Lower"] <= i) & (ar_threshold["Upper"] > i)),
                        "IV_performance",
                    ].values[0]
                    for i in df_stat["ar"].to_list()
                ]
            df_stat["iv"] = woe_engine.information_value(woe_df=df_woe)
            if iv_threshold is not None:
                df_stat["soglia_iv"] = [
                    iv_threshold.loc[
                        ((iv_threshold["Lower"] <= i) & (iv_threshold["Upper"] > i)),
                        "IV_performance",
                    ].values[0]
                    for i in df_stat["iv"].to_list()
                ]
            out = pd.concat([out, df_stat], axis=0)

        return out, df_proc_woe
