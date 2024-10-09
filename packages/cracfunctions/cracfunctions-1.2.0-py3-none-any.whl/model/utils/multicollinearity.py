from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd
from typing import List


class Multicollinearity:
    @staticmethod
    def compute_vif(ind_df: pd.DataFrame, col: List[str]) -> pd.DataFrame:
        df = ind_df[col]
        for c in col:
            df = df[(df[c].isnull() == False)]
        df_vix = pd.DataFrame()
        df_vix["indicator"] = col
        df_vix["vif"] = (
            None
            if df.shape[1] <= 1
            else [
                variance_inflation_factor(exog=df.values, exog_idx=i)
                for i in range(len(df.columns))
            ]
        )

        return df_vix
