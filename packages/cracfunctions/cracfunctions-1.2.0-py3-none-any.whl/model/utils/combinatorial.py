import pandas as pd
from enum import Enum
from typing import List, Callable, Dict, Union
from itertools import combinations
from sklearn.linear_model import LogisticRegression, LinearRegression
from tqdm import tqdm
from joblib import Parallel, delayed
from model.utils.regression_model import LogisticEngine, ModelOut
from functools import partial
from multiprocessing import Pool
import numpy as np
from statsmodels.discrete.discrete_model import BinaryResultsWrapper


class ModelType(Enum):
    LINEAR_REGRESSION = "LINEAR_REGRESSION"
    LOGISTIC_REGRESSION = "LOGISTIC_REGRESSION"


class CombinatorialEngine:
    def __init__(
        self, model: ModelType, min_n_variable: int = 2, max_n_variable: int = 10
    ) -> None:
        self._model = model
        self._min_n_variable = min_n_variable
        self._max_n_variable = max_n_variable

    @property
    def model(
        self,
    ) -> None:
        return self._model

    @property
    def min_n_variable(
        self,
    ) -> None:
        return self._min_n_variable

    @property
    def max_n_variable(
        self,
    ) -> None:
        return self._max_n_variable

    def _define_model(
        self, target: pd.DataFrame, significance_level: float = 0.05
    ) -> Callable:
        if self._model == ModelType.LOGISTIC_REGRESSION:
            return partial(
                LogisticEngine(significance_level=significance_level).fit,
                target=target,
            )

    @staticmethod
    def _filter_area(variables_dict: Dict[str, str], target_list: List) -> List:
        check_area = list(set([variables_dict[i] for i in target_list]))
        if len(check_area) < len(target_list):
            return [""]
        return target_list

    def create_model_list(
        self, ind_df: pd.DataFrame, variables: Dict[str, str]
    ) -> List[str]:
        model_list = []
        for n in tqdm(
            range(self._min_n_variable, self._max_n_variable + 1),
            desc="Model list creation",
            ascii=True,
        ):
            model_list += [
                self._filter_area(variables_dict=variables, target_list=list(i))
                for i in combinations(iterable=sorted(list(variables.keys())), r=n)
            ]
        model_list = [i for i in model_list if i != [""]]
        return model_list

    def create_models(
        self,
        ind_df: pd.DataFrame,
        target_var: str,
        model_list: List[List[str]],
        significance_level: float = 0.05,
    ) -> List[ModelOut]:
        fit_model = self._define_model(
            target=ind_df[target_var], significance_level=significance_level
        )
        with Parallel(n_jobs=-1, backend="threading") as parallel:
            models = parallel(
                delayed(fit_model)(ind_df[m])
                for m in tqdm(model_list, desc="Model fit status", ascii=True)
            )
        return models
