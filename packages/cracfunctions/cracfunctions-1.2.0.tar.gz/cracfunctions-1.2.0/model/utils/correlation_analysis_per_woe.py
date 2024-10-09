import pandas as pd
from typing import Tuple, List


def main(
    perim: pd.DataFrame,
    var_list: List,
) -> Tuple[pd.DataFrame]:
    correlation_matrix_pearson = perim[var_list].corr(method="pearson")
    correlation_matrix_spearman = perim[var_list].corr(method="spearman")
    return correlation_matrix_pearson, correlation_matrix_spearman
