import pandas as pd
from scipy import stats
import numpy as np
from string import Template
from typing import Dict


class TestStat:
    @staticmethod
    def compute_dr(
        ind_df: pd.DataFrame, var_col: str, default_col: str
    ) -> pd.DataFrame:
        dr = (
            (
                ind_df[[var_col, default_col]]
                .groupby(by=var_col, dropna=False)[default_col]
                .agg({"count", "sum"})
            )
            .reset_index()
            .rename(columns={"sum": "n_def", "count": "n"})
        )
        dr["dr"] = dr.n_def / dr.n
        dr.sort_values(by=var_col, inplace=True)
        return dr

    def test_monotonicity_dr(
        self, ind_df: pd.DataFrame, var_col: str, default_col: str
    ) -> bool:
        dr = self.compute_dr(ind_df=ind_df, var_col=var_col, default_col=default_col)
        check_monotonicity = (
            dr.dr.is_monotonic_increasing or dr.dr.is_monotonic_decreasing
        )
        return check_monotonicity

    def t_test(
        self,
        ind_df: pd.DataFrame,
        var_col: str,
        default_col: str,
        t_test_threshold: float,
    ) -> bool:
        dr = self.compute_dr(ind_df=ind_df, var_col=var_col, default_col=default_col)
        for i in range(dr.shape[0] - 1):
            var_i = dr.loc[i, "dr"] * (1 - dr.loc[i, "dr"])
            var_i_1 = dr.loc[i + 1, "dr"] * (1 - dr.loc[i + 1, "dr"])
            t_statistic = (dr.loc[i + 1, "dr"] - dr.loc[i, "dr"]) / np.sqrt(
                var_i_1 / dr.loc[i + 1, "n"] + var_i / dr.loc[i, "n"]
            )
            if t_statistic < t_test_threshold:
                return False
        return True

    @staticmethod
    def test_hhi(
        ind_df: pd.DataFrame,
        var_col: str,
        default_col: str,
        hhi_map: Dict[str, Template],
    ) -> str:
        hhi_df = (
            (
                ind_df[[var_col, default_col]]
                .groupby(by=var_col, dropna=False)[default_col]
                .agg({"count"})
            )
            .reset_index()
            .rename(columns={"count": "n"})
        )
        hhi = sum((hhi_df.n / hhi_df.n.sum()) ** 2)
        hhi = (hhi - 1 / hhi_df.shape[0]) / (1 - 1 / hhi_df.shape[0])
        for k, v in hhi_map.items():
            if eval(v.substitute(hhi=hhi)):
                return k
