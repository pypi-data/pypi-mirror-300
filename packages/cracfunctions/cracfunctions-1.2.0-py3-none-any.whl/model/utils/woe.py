import pandas as pandas
from enum import Enum
from typing import List
import numpy as np
import pandas as pd
from model.utils.check_missing import check_missing


class CreditType(Enum):
    BONIS = "BONIS"
    DEFAULT = "DEFAULT"


class WOEEngine:
    def __init__(self, min_den_value: float = 1e-4):
        self._min_den_value = min_den_value

    @property
    def min_den_value(
        self,
    ) -> float:
        return self._min_den_value

    @staticmethod
    def perc_calc(
        ind_df: pd.DataFrame,
        ind_name: str,
        credit_type: CreditType,
        def_col: str = "default",
    ) -> pd.DataFrame:
        if credit_type == CreditType.BONIS:
            stat = (
                ind_df.loc[(ind_df[def_col] == 0.0), [ind_name, def_col]]
                .groupby(by=[ind_name])[def_col]
                .count()
                .reset_index()
                .rename(columns={def_col: "n_bonis"})
            )
            stat["n_bonis_perc"] = (
                stat["n_bonis"] / ind_df[(ind_df[def_col] == 0.0)].shape[0]
            )
        else:
            stat = (
                ind_df.loc[(ind_df[def_col] == 1.0), [ind_name, def_col]]
                .groupby(by=[ind_name])[def_col]
                .count()
                .reset_index()
                .rename(columns={def_col: "n_default"})
            )
            stat["n_default_perc"] = (
                stat["n_default"] / ind_df[(ind_df[def_col] == 1.0)].shape[0]
            )
        return stat

    def woe_calc(
        self, ind_df: pd.DataFrame, ind_name: str, def_col: str = "default"
    ) -> pd.DataFrame:
        perc_bonis = self.perc_calc(
            ind_df=ind_df,
            ind_name=ind_name,
            credit_type=CreditType.BONIS,
            def_col=def_col,
        )
        perc_default = self.perc_calc(
            ind_df=ind_df,
            ind_name=ind_name,
            credit_type=CreditType.DEFAULT,
            def_col=def_col,
        )
        perc = pd.merge(perc_bonis, perc_default, how="left", on=ind_name)

        # Fix missing values
        perc.n_bonis = [0 if check_missing(i) else i for i in perc.n_bonis.to_list()]
        perc.n_bonis_perc = [
            0 if check_missing(i) else i for i in perc.n_bonis_perc.to_list()
        ]
        perc.n_default = [
            0 if check_missing(i) else i for i in perc.n_default.to_list()
        ]
        perc.n_default_perc = [
            self._min_den_value if check_missing(i) else i
            for i in perc.n_default_perc.to_list()
        ]

        perc["woe"] = np.log(perc.n_bonis_perc / perc.n_default_perc)
        perc.rename(columns={ind_name: "indicator_value"}, inplace=True)
        perc = pd.concat(
            [
                pd.DataFrame(
                    {"indicator_name": np.repeat(ind_name, int(perc.shape[0]))}
                ),
                perc,
            ],
            axis=1,
        )

        return perc

    def information_value(self, woe_df: pd.DataFrame) -> float:
        return sum((woe_df.n_bonis_perc - woe_df.n_default_perc) * woe_df.woe)
