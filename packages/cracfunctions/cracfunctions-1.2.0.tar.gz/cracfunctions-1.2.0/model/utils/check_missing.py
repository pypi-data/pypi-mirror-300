import numpy as np
from typing import Union, Dict
import math
import pandas as pd
from copy import deepcopy


def missing_classification(
    total_df: pd.DataFrame, missing_dict: Dict[str, object]
) -> (pd.DataFrame, pd.DataFrame):
    """
    Returns the division between the integral-missing df and the non-integral-missing df
    based on the missing_dict in input
    """
    missing_class_df = deepcopy(total_df)
    condition = pd.Series(True, index=missing_class_df.index)
    for ind in missing_dict.keys():
        condition = condition & (missing_class_df[ind] == missing_dict[ind])
    integral_missing_df = missing_class_df[condition]
    no_integral_missing_df = missing_class_df.drop(integral_missing_df.index)
    return (integral_missing_df, no_integral_missing_df)


def check_missing(
    x: Union[float, str, np.ndarray, pd.Series]
) -> Union[bool, np.ndarray, pd.Series]:
    # Working with x as a vector
    if isinstance(x, np.ndarray):
        return np.isnan(x)
    if isinstance(x, pd.Series):
        return x.isnull()

    # Working with x as a single element
    try:
        if x is None:
            return True

    except:
        ...
    try:
        if x == np.nan:
            return True
    except:
        ...
    try:
        if math.isnan(x):
            return True
    except:
        ...
    try:
        if x is pd.NA:
            return True
    except:
        ...

    return False
