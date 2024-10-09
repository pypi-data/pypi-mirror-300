import pandas as pd
from typing import List, Tuple
import numpy as np
from enum import Enum
from model.balance_sheet_module.utils.indeterminate_forms import (
    IndeterminateFormsMapOutput,
)
from model.utils.accuracy import AccuracyEngine
from typing import Tuple, Optional
from dataclasses import dataclass
from polars import DataFrame, col
import polars as pl
import time
from model.utils.percentiles import PercentileEngine, InterpolationType


class UShapeType(Enum):
    USHAPE_UP = "USHAPE_UP"
    USHAPE_DOWN = "USHAPE_DOWN"
    NO_USHAPE = "NO_USHAPE"


@dataclass
class UShapeTreatmentParam:
    percentile_perc: Optional[float] = None
    percentile_value: Optional[float] = None


class UShapeEngine:
    """Class for the U-shape identification and treatment application"""

    def __init__(
        self,
        buckets_bounds: List[Tuple[float]] = [(0.0, 0.25), (0.25, 0.75), (0.75, 1.0)],
        interpolation_type: InterpolationType = InterpolationType.GE_THRESHOLD,
    ) -> None:
        self._buckets_bounds = sorted(buckets_bounds)
        self._interpolation_type = interpolation_type

    @property
    def buckets_bounds(
        self,
    ) -> List:
        return self._buckets_bounds

    @property
    def interpolation_type(self) -> InterpolationType:
        return self._interpolation_type

    def update_interpolation_type(self, interpolation_type: InterpolationType) -> None:
        self._interpolation_type = interpolation_type

    def percentile_engine(self) -> PercentileEngine:
        return PercentileEngine(interpolation_type=self._interpolation_type)

    def identify(
        self,
        ind_perim: pd.DataFrame,
        ind_col: str,
        default_col: str = "default",
        threshold: float = 0.15,
    ) -> UShapeType:
        ind_perim_no_88_99 = ind_perim[
            (
                (ind_perim[ind_col] != IndeterminateFormsMapOutput.V_99999999.value)
                & (ind_perim[ind_col] != IndeterminateFormsMapOutput.V_88888888.value)
            )
        ]

        dr_bucket = {
            i: ind_perim_no_88_99.loc[
                (
                    (
                        ind_perim_no_88_99[ind_col]
                        >= self.percentile_engine().compute_percentile(
                            x=ind_perim_no_88_99[ind_col].to_numpy(), percentile=i[0]
                        )
                    )
                    & (
                        ind_perim_no_88_99[ind_col]
                        <= self.percentile_engine().compute_percentile(
                            x=ind_perim_no_88_99[ind_col].to_numpy(), percentile=i[1]
                        )
                    )
                ),
                [ind_col, default_col],
            ]
            if index_ == 0
            else ind_perim_no_88_99.loc[
                (
                    (
                        ind_perim_no_88_99[ind_col]
                        > self.percentile_engine().compute_percentile(
                            x=ind_perim_no_88_99[ind_col].to_numpy(), percentile=i[0]
                        )
                    )
                    & (
                        ind_perim_no_88_99[ind_col]
                        <= self.percentile_engine().compute_percentile(
                            x=ind_perim_no_88_99[ind_col].to_numpy(), percentile=i[1]
                        )
                    )
                ),
                [ind_col, default_col],
            ]
            for index_, i in enumerate(self._buckets_bounds)
        }
        dr_bucket = {k: v[default_col].sum() / v.shape[0] for k, v in dr_bucket.items()}
        list_dr_bucket = list(dr_bucket.values())
        delta_left = (list_dr_bucket[1] - list_dr_bucket[0]) / list_dr_bucket[0]

        delta_right = (list_dr_bucket[-1] - list_dr_bucket[-2]) / list_dr_bucket[-2]
        if delta_left < -threshold and delta_right > threshold:
            return UShapeType.USHAPE_UP
        elif delta_left > threshold and delta_right < -threshold:
            return UShapeType.USHAPE_DOWN
        else:
            return UShapeType.NO_USHAPE

    def estimate_apply_quadratic_transformation(
        self,
        ind_df: pd.DataFrame,
        indicator_name: str,
        direction: int,
        list_indet_forms: List[IndeterminateFormsMapOutput] = [
            IndeterminateFormsMapOutput.V_99999999,
            IndeterminateFormsMapOutput.V_88888888,
            IndeterminateFormsMapOutput.V_N_100000000,
            IndeterminateFormsMapOutput.V_P_100000000,
        ],
        default_col: str = "default",
        round_digit: int = 9,
    ) -> Tuple[np.ndarray, UShapeTreatmentParam]:
        """Estimate and apply u-shape parameters"""

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

        # Exclude 88/99 forms
        ind_perim_no_88_99 = ind_df[
            (
                (ind_df[indicator_name] != IndeterminateFormsMapOutput.V_99999999.value)
                & (
                    ind_df[indicator_name]
                    != IndeterminateFormsMapOutput.V_88888888.value
                )
            )
        ]

        k_list = list(np.linspace(0.0, 1.0, 101))
        percentiles_dict = {
            k: self.percentile_engine().compute_percentile(
                x=ind_perim_no_88_99[indicator_name].to_numpy(), percentile=k
            )
            for k in k_list
            if self.percentile_engine().compute_percentile(
                x=ind_perim_no_88_99[indicator_name].to_numpy(), percentile=k
            )
            not in [
                neg_mln,
                pos_mln,
            ]
        }
        sim_df = {
            k: np.where(
                (
                    (
                        ind_df[indicator_name]
                        != IndeterminateFormsMapOutput.V_88888888.value
                    )
                    & (
                        ind_df[indicator_name]
                        != IndeterminateFormsMapOutput.V_99999999.value
                    )
                    & (ind_df[indicator_name] != neg_mln)
                    & (ind_df[indicator_name] != pos_mln)
                ),
                (ind_df[indicator_name] - percentile) ** 2,
                ind_df[indicator_name],
            )
            for k, percentile in percentiles_dict.items()
        }
        sim_df = {
            k: np.where(
                x == neg_mln,
                pos_mln,
                x,
            )
            for k, x in sim_df.items()
        }
        ar = {
            k: AccuracyEngine().compute_somersd(x=x, y=ind_df[default_col].to_numpy())
            for k, x in sim_df.items()
        }
        max_ar_ind_adj = {
            k: sim_df[k]
            for k, v in ar.items()
            if v * direction == min(np.array(list(ar.values())) * direction)
        }

        return (
            list(np.round(list(max_ar_ind_adj.values())[0], round_digit)),
            UShapeTreatmentParam(
                percentile_perc=round(list(max_ar_ind_adj.keys())[0], round_digit),
                percentile_value=round(
                    self.percentile_engine().compute_percentile(
                        x=ind_perim_no_88_99[indicator_name].to_numpy(),
                        percentile=list(max_ar_ind_adj.keys())[0],
                    ),
                    round_digit,
                ),
            ),
        )

    @staticmethod
    def apply_quadratic_transformation(
        ind_df: pd.DataFrame,
        ushape_param: float,
        indicator_name: str,
        list_indet_forms: List[IndeterminateFormsMapOutput],
    ) -> np.ndarray:
        """Apply u-shape parameters"""
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
        result = np.where(
            (
                (ind_df[indicator_name] != IndeterminateFormsMapOutput.V_88888888.value)
                & (
                    ind_df[indicator_name]
                    != IndeterminateFormsMapOutput.V_99999999.value
                )
                & (ind_df[indicator_name] != neg_mln)
                & (ind_df[indicator_name] != pos_mln)
            ),
            (ind_df[indicator_name] - ushape_param) ** 2,
            ind_df[indicator_name],
        )
        result = np.where(result == neg_mln, pos_mln, result)
        return result
