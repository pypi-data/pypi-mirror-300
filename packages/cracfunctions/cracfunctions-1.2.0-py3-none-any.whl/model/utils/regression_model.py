import pandas as pd
from enum import Enum
from typing import Dict
from model.utils.percentiles import PercentileEngine, InterpolationType
from model.balance_sheet_module.utils.indeterminate_forms import (
    IndeterminateFormsMapOutput,
)
import numpy as np
from typing import List, Tuple, Union
from sklearn.linear_model import LogisticRegression, LinearRegression
import warnings
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import BinaryResultsWrapper
from abc import ABC, abstractmethod
from dataclasses import dataclass
from model.utils.accuracy import AccuracyEngine
from model.utils.multicollinearity import Multicollinearity


class RegressionModelBase(ABC):
    def __init__(self, significance_level: float = 0.05) -> None:
        self._significance_level = significance_level

    @property
    def significance_level(
        self,
    ) -> float:
        return self._significance_level

    @abstractmethod
    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> Dict[str, object]:
        ...

    @staticmethod
    def compute_accuracy(score: np.ndarray, target_var: np.ndarray) -> float:
        return AccuracyEngine().compute_somersd(x=score, y=target_var)

    @staticmethod
    def compute_vif(features: pd.DataFrame) -> pd.DataFrame:
        return Multicollinearity().compute_vif(
            ind_df=features, col=list(features.columns)
        )


TYPE_MODEL = Union[LogisticRegression, LinearRegression, BinaryResultsWrapper]


@dataclass
class ModelOut:
    model: TYPE_MODEL
    model_report: pd.DataFrame


class CutOffType(Enum):
    LOWER = "LOWER"
    UPPER = "UPPER"


class LogisticParameter(Enum):
    CENTER = "CENTER"
    SLOPE = "SLOPE"
    MEAN = "MEAN"
    STDEV = "STDEV"


class LogisticEngine(RegressionModelBase):
    def __init__(
        self,
        significance_level: float = 0.005,
        cutoff_multiplier: float = 1.5,
        slope_num: float = 2.95,
        interpolation_type: InterpolationType = InterpolationType.GE_THRESHOLD,
    ) -> None:
        super().__init__(significance_level=significance_level)
        self._cutoff_multiplier = cutoff_multiplier
        self._slope_num = slope_num
        self._interpolation_type = interpolation_type

    @property
    def cutoff_multiplier(
        self,
    ) -> float:
        return self._cutoff_multiplier

    @property
    def slope_num(
        self,
    ) -> float:
        return self._slope_num

    @property
    def interpolation_type(
        self,
    ) -> InterpolationType:
        return self._interpolation_type

    def cutoff_identification(
        self,
        ind: np.ndarray,
    ) -> Dict[CutOffType, float]:
        percentiles = PercentileEngine(
            interpolation_type=self._interpolation_type
        ).compute_percentile(
            x=ind, percentile=list(np.round(np.linspace(0.0, 1.0, 101), 2))
        )
        lower = percentiles[0.25] - self._cutoff_multiplier * (
            percentiles[0.75] - percentiles[0.25]
        )
        upper = percentiles[0.75] + self._cutoff_multiplier * (
            percentiles[0.75] - percentiles[0.25]
        )
        # Approximate the parameters to the closer percentile
        # Lower
        lower_adj = {p: abs(lower - v) for p, v in percentiles.items()}
        min_delta = [
            p for p, v in lower_adj.items() if v == min(list(lower_adj.values()))
        ][0]
        lower_adj = (
            percentiles[min_delta]
            if lower <= percentiles[min_delta]
            else percentiles[round(min_delta + 0.01, 2)]
        )
        # Upper
        upper_adj = {p: abs(upper - v) for p, v in percentiles.items()}
        min_delta = [
            p for p, v in upper_adj.items() if v == min(list(upper_adj.values()))
        ][0]
        upper_adj = (
            percentiles[min_delta]
            if upper >= percentiles[min_delta]
            else percentiles[round(min_delta - 0.01, 2)]
        )

        return {
            CutOffType.LOWER: lower_adj,
            CutOffType.UPPER: upper_adj,
        }

    def estimate_parameter(
        self, cutoff: Dict[CutOffType, float]
    ) -> Dict[LogisticParameter, float]:
        center = (cutoff[CutOffType.LOWER] + cutoff[CutOffType.UPPER]) / 2.0
        slope = self._slope_num / (cutoff[CutOffType.LOWER] - center)
        return {LogisticParameter.CENTER: center, LogisticParameter.SLOPE: slope}

    def estimate_apply_logistic_transformation(
        self,
        ind_df: pd.DataFrame,
        ind_col: str,
        standard_deviation_target: float = 50,
        list_indet_forms: List[IndeterminateFormsMapOutput] = [
            IndeterminateFormsMapOutput.V_99999999,
            IndeterminateFormsMapOutput.V_88888888,
            IndeterminateFormsMapOutput.V_N_100000000,
            IndeterminateFormsMapOutput.V_P_100000000,
        ],
    ) -> Tuple[np.ndarray, Dict[LogisticParameter, float]]:
        # Select mln variable
        neg_mln = (
            IndeterminateFormsMapOutput.V_N_100000000.value
            if IndeterminateFormsMapOutput.V_N_100000000 in list_indet_forms
            else IndeterminateFormsMapOutput.V_N_1000000.value
        )
        pos_mln = (
            IndeterminateFormsMapOutput.V_P_100000000.value
            if IndeterminateFormsMapOutput.V_P_100000000 in list_indet_forms
            else IndeterminateFormsMapOutput.V_P_1000000.value
        )
        # Remove +/mln and 99 from the estimation of the logistic parameters
        ind = ind_df[
            (
                (ind_df[ind_col] != neg_mln)
                & (ind_df[ind_col] != pos_mln)
                & (ind_df[ind_col] != IndeterminateFormsMapOutput.V_99999999.value)
            )
        ]
        ind = ind[ind_col].to_numpy()

        # Estimate parameters
        logistic_param = self.estimate_parameter(
            cutoff=self.cutoff_identification(ind=ind)
        )
        exponent = logistic_param[LogisticParameter.SLOPE] * (
            logistic_param[LogisticParameter.CENTER] - ind_df[ind_col]
        )
        logistic_ind = np.where(
            (
                (ind_df[ind_col] != IndeterminateFormsMapOutput.V_99999999.value)
                & (exponent <= 700)
            ),
            1 / (1 + np.exp(exponent)),
            ind_df[ind_col],
        )
        logistic_ind = np.where(
            (
                (ind_df[ind_col] != IndeterminateFormsMapOutput.V_99999999.value)
                & (exponent > 700)
            ),
            0.0,
            logistic_ind,
        )

        # Standardized parameters
        logistic_param[LogisticParameter.MEAN] = logistic_ind[
            (logistic_ind != IndeterminateFormsMapOutput.V_99999999.value)
        ].mean()
        logistic_param[LogisticParameter.STDEV] = np.std(
            logistic_ind[(logistic_ind != IndeterminateFormsMapOutput.V_99999999.value)]
        )

        logistic_ind_normalized = np.where(
            logistic_ind != IndeterminateFormsMapOutput.V_99999999.value,
            standard_deviation_target
            * (logistic_ind - logistic_param[LogisticParameter.MEAN])
            / logistic_param[LogisticParameter.STDEV],
            logistic_ind,
        )
        return logistic_ind_normalized, logistic_param

    def apply_logistic_transformation(
        self,
        ind_df: pd.DataFrame,
        ind_col: str,
        slope: float,
        center: float,
        std_mean: float,
        std_stdev: float,
        standard_deviation_target: float = 50,
        list_indet_forms: List[IndeterminateFormsMapOutput] = [
            IndeterminateFormsMapOutput.V_99999999,
            IndeterminateFormsMapOutput.V_88888888,
            IndeterminateFormsMapOutput.V_N_100000000,
            IndeterminateFormsMapOutput.V_P_100000000,
        ],
    ) -> np.ndarray:
        # Select mln variable
        neg_mln = (
            IndeterminateFormsMapOutput.V_N_100000000.value
            if IndeterminateFormsMapOutput.V_N_100000000 in list_indet_forms
            else IndeterminateFormsMapOutput.V_N_1000000.value
        )
        pos_mln = (
            IndeterminateFormsMapOutput.V_P_100000000.value
            if IndeterminateFormsMapOutput.V_P_100000000 in list_indet_forms
            else IndeterminateFormsMapOutput.V_P_1000000.value
        )
        exponent = slope * (center - ind_df[ind_col])
        logistic_ind = np.where(
            (
                (ind_df[ind_col] != IndeterminateFormsMapOutput.V_99999999.value)
                & (exponent <= 700)
            ),
            1 / (1 + np.exp(exponent)),
            ind_df[ind_col],
        )
        logistic_ind = np.where(
            (
                (ind_df[ind_col] != IndeterminateFormsMapOutput.V_99999999.value)
                & (exponent > 700)
            ),
            0.0,
            logistic_ind,
        )

        logistic_ind_normalized = np.where(
            logistic_ind != IndeterminateFormsMapOutput.V_99999999.value,
            standard_deviation_target * (logistic_ind - std_mean) / std_stdev,
            logistic_ind,
        )
        return logistic_ind_normalized

    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> ModelOut:
        # Ignore warnings during the model fitting
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            constant = sm.add_constant(features)
            model = sm.Logit(endog=target.astype(int), exog=constant)
            model = model.fit(disp=False)
        return ModelOut(
            model=model,
            model_report=self.model_report(
                features=features, target=target, model=model
            ),
        )

    def standardized_coef(
        self, features: pd.DataFrame, model: BinaryResultsWrapper
    ) -> pd.DataFrame:
        return model.params[1:] * features.std().values * np.sqrt(3) / np.pi

    def create_scores(self, model: BinaryResultsWrapper) -> np.ndarray:
        probability = model.predict()
        score = np.log(probability / (1 - probability))
        return score

    def compute_hhi(self, summary: pd.DataFrame) -> None:
        w2 = np.sum(summary.weights**2)
        n_significant = summary.loc[1:, "p_values"]
        n_significant = n_significant[n_significant <= self._significance_level].shape[
            0
        ]
        summary["hhi"] = (
            np.nan
            if n_significant == 0
            else (w2 - (1 / n_significant)) / (1 - (1 / n_significant))
        )

    def model_report(
        self, features: pd.DataFrame, target: pd.DataFrame, model: BinaryResultsWrapper
    ) -> pd.DataFrame:
        summary = pd.DataFrame(
            {
                "parameter": ["intercept"] + list(features.columns),
                "estimate": model.params.to_list(),
                "std_error": model.bse.to_list(),
                "wald": ((model.params / model.bse) ** 2).to_list(),
                "p_values": model.pvalues.to_list(),
                "standardized_estimate": [None]
                + self.standardized_coef(features=features, model=model).to_list(),
            }
        )
        summary["weights"] = np.abs(summary.standardized_estimate) / np.sum(
            np.abs(summary.standardized_estimate)
        )
        self.compute_hhi(summary=summary)
        summary["ar"] = self.compute_accuracy(
            score=self.create_scores(model=model),
            target_var=target.to_numpy(),
        )
        summary = summary.merge(
            self.compute_vif(features=features),
            how="left",
            left_on="parameter",
            right_on="indicator",
        )
        summary.drop("indicator", axis=1, inplace=True)

        return summary
