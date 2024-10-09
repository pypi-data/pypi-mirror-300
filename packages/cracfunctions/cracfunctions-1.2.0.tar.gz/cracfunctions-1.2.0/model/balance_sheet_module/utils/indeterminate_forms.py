from enum import Enum
from typing import Dict, Optional, List, Tuple
import numpy as np
import pandas as pd
from copy import deepcopy
from dataclasses import dataclass
from model.utils.percentiles import PercentileEngine, InterpolationType


class IndeterminateForms(Enum):
    """Types of indeterminate forms"""

    DN_NN = "Negative denominator - Negative numerator"
    DN_NP = "Negative denominator - Positive numerator"
    DN_N0 = "Negative denominator - Numerator equals zero"
    D0_NN = "Denominator equals zero - Negative numerator"
    D0_NP = "Denominator equals zero - Positive numerator"
    D0_N0 = "Denominator equals zero - Numerator equals zero"
    DP_NN = "Positive denominator - Negative numerator"
    DP_NP = "Positive denominator - Positive numerator"
    DP_N0 = "Positive denominator - Numerator equals zero"


@dataclass
class Param88Treatment:
    param: Optional[float] = None
    perc_bucket_pop: Optional[Dict[Tuple[float], float]] = None


class IndeterminateFormsMapOutput(Enum):
    V_99999999 = 99999999
    V_P_100000000 = 100000000
    V_N_100000000 = -100000000
    V_P_1000000 = 1000000
    V_N_1000000 = -1000000
    V_88888888 = 88888888


class IndeterminateFormsEngine:
    def __init__(
        self,
        interpolation_type: InterpolationType = InterpolationType.GE_THRESHOLD,
    ) -> None:
        self._interpolation_type = interpolation_type

    """Class for the indeterminate forms treatment"""

    @property
    def interpolation_type(self) -> InterpolationType:
        return self._interpolation_type

    def update_interpolation_type(self, interpolation_type: InterpolationType) -> None:
        self._interpolation_type = interpolation_type

    def percentile_engine(self) -> PercentileEngine:
        return PercentileEngine(interpolation_type=self._interpolation_type)

    @staticmethod
    def apply_map(
        num: np.ndarray,
        den: np.ndarray,
        indeterminate_forms_map: Dict[IndeterminateForms, Optional[float]],
        round_digit: int = 9,
    ) -> np.ndarray:
        """Map application of the indeterminate forms"""
        x = np.column_stack((num, den))
        x = pd.DataFrame(x, columns=["num", "den"])
        cond_none = (x.den.isnull() == True) | (x.num.isnull() == True)
        cond_den_neg = x.den < 0.0
        cond_den_0 = x.den == 0.0
        cond_den_pos = x.den > 0.0
        cond_num_neg = x.num < 0.0
        cond_num_0 = x.num == 0.0
        cond_num_pos = x.num > 0.0
        x["ind_calc"] = x.num / x.den
        x["ind_final"] = x.ind_calc

        # All the conditions on the numerator and the denominator are checked when
        # both are not missing

        # Negative denominator
        x.ind_final = np.where(
            (cond_none == False) & (cond_den_neg) & (cond_num_neg),
            indeterminate_forms_map[IndeterminateForms.DN_NN],
            x.ind_final,
        )
        x.ind_final = np.where(
            (cond_none == False) & (cond_den_neg) & (cond_num_pos),
            indeterminate_forms_map[IndeterminateForms.DN_NP],
            x.ind_final,
        )
        x.ind_final = np.where(
            (cond_none == False) & (cond_den_neg) & (cond_num_0),
            indeterminate_forms_map[IndeterminateForms.DN_N0],
            x.ind_final,
        )
        # Denominator equals to zero
        x.ind_final = np.where(
            (cond_none == False) & (cond_den_0) & (cond_num_neg),
            indeterminate_forms_map[IndeterminateForms.D0_NN],
            x.ind_final,
        )
        x.ind_final = np.where(
            (cond_none == False) & (cond_den_0) & (cond_num_pos),
            indeterminate_forms_map[IndeterminateForms.D0_NP],
            x.ind_final,
        )
        x.ind_final = np.where(
            (cond_none == False) & (cond_den_0) & (cond_num_0),
            indeterminate_forms_map[IndeterminateForms.D0_N0],
            x.ind_final,
        )
        # Positive denominator
        x.ind_final = np.where(
            (cond_none == False) & (cond_den_pos) & (cond_num_neg),
            indeterminate_forms_map[IndeterminateForms.DP_NN],
            x.ind_final,
        )
        x.ind_final = np.where(
            (cond_none == False) & (cond_den_pos) & (cond_num_pos),
            indeterminate_forms_map[IndeterminateForms.DP_NP],
            x.ind_final,
        )
        x.ind_final = np.where(
            (cond_none == False) & (cond_den_pos) & (cond_num_0),
            indeterminate_forms_map[IndeterminateForms.DP_N0],
            x.ind_final,
        )

        # Convert the COMPUTE_VALUE
        # If the mapped cases are null then the calculated values are used
        x.ind_final = np.where(
            x.ind_final.isnull() == True,
            x.ind_calc,
            x.ind_final,
        )
        # If also the calculated value is None the 99999999 is used
        x.ind_final = np.where(
            x.ind_final.isnull() == True,
            IndeterminateFormsMapOutput.V_99999999.value,
            x.ind_final,
        )
        x.ind_final = [round(i, round_digit) for i in x.ind_final.to_list()]
        return x.ind_final.to_numpy()

    def v_88888888_treatment(
        self,
        ind_df: pd.DataFrame,
        ind_col: str,
        buckets_bounds: List[Tuple[float]],
        list_indet_forms: List[IndeterminateFormsMapOutput],
        default_col: str = "default",
        round_digit: int = 9,
    ) -> Tuple[np.ndarray, Param88Treatment]:
        """Estimate and apply 88 treatment"""
        # Select mln variable
        neg_mln = (
            IndeterminateFormsMapOutput.V_N_100000000
            if IndeterminateFormsMapOutput.V_N_100000000 in list_indet_forms
            else IndeterminateFormsMapOutput.V_N_1000000
        )
        pos_mln = (
            IndeterminateFormsMapOutput.V_P_100000000
            if IndeterminateFormsMapOutput.V_P_100000000 in list_indet_forms
            else IndeterminateFormsMapOutput.V_P_1000000
        )

        output = deepcopy(ind_df)
        # Filter 99999999
        p_no_99 = output[
            (output[ind_col] != IndeterminateFormsMapOutput.V_99999999.value)
        ]

        # DR 88888888
        if (
            IndeterminateFormsMapOutput.V_88888888.value
            not in output[ind_col].to_list()
        ):
            return output, Param88Treatment(
                perc_bucket_pop={k: None for k in buckets_bounds}
            )
        dr_88 = (
            output.loc[
                (output[ind_col] == IndeterminateFormsMapOutput.V_88888888.value),
                default_col,
            ].sum()
            / output.loc[
                (output[ind_col] == IndeterminateFormsMapOutput.V_88888888.value)
            ].shape[0]
        )

        # DR
        p_no_99_88 = p_no_99[
            (p_no_99[ind_col] != IndeterminateFormsMapOutput.V_88888888.value)
        ]

        dr_intervals = {}
        size_intervals = {}
        for index_, i in enumerate(buckets_bounds):
            left_lim = self.percentile_engine().compute_percentile(
                x=p_no_99_88[ind_col].to_numpy(), percentile=i[0]
            )
            right_lim = self.percentile_engine().compute_percentile(
                x=p_no_99_88[ind_col].to_numpy(), percentile=i[1]
            )
            if (index_ == 0) | (left_lim == right_lim):
                size_intervals[i] = p_no_99_88.loc[
                    (
                        (p_no_99_88[ind_col] >= left_lim)
                        & (p_no_99_88[ind_col] <= right_lim)
                    ),
                    default_col,
                ].shape[0]
                dr_intervals[i] = abs(
                    (
                        p_no_99_88.loc[
                            (
                                (p_no_99_88[ind_col] >= left_lim)
                                & (p_no_99_88[ind_col] <= right_lim)
                            ),
                            default_col,
                        ].sum()
                        / size_intervals[i]
                    )
                    - dr_88
                )
            else:
                size_intervals[i] = p_no_99_88.loc[
                    (
                        (p_no_99_88[ind_col] > left_lim)
                        & (p_no_99_88[ind_col] <= right_lim)
                    ),
                    default_col,
                ].shape[0]
                dr_intervals[i] = abs(
                    (
                        p_no_99_88.loc[
                            (
                                (p_no_99_88[ind_col] > left_lim)
                                & (p_no_99_88[ind_col] <= right_lim)
                            ),
                            default_col,
                        ].sum()
                        / size_intervals[i]
                    )
                    - dr_88
                )

        bucket_list = [
            k for k, v in dr_intervals.items() if v == min(dr_intervals.values())
        ]
        # If two or more buckets are made by the same sample:
        # 1) If the dimensions of the intervals are the same then the median is chosen
        # 2) If the dimensions of the intervals are different, then choose the first in line with SAS
        if (
            len(bucket_list)
            > 1 & len(list(set([size_intervals[i] for i in bucket_list])))
            == 1.0
        ):
            v_sub_88 = round(p_no_99_88[ind_col].median(), round_digit)
        else:
            bucket = bucket_list[0]
            if bucket == buckets_bounds[0]:
                v_sub_88 = neg_mln.value
            elif bucket == buckets_bounds[-1]:
                v_sub_88 = pos_mln.value
            else:
                v_sub_88 = round(p_no_99_88[ind_col].median(), round_digit)
        output[ind_col] = np.where(
            output[ind_col] == IndeterminateFormsMapOutput.V_88888888.value,
            v_sub_88,
            output[ind_col].to_numpy(),
        )
        return (
            output[ind_col].to_numpy(),
            Param88Treatment(param=v_sub_88, perc_bucket_pop=size_intervals),
        )

    @staticmethod
    def apply_v_88888888_treatment(
        ind_df: pd.DataFrame, ind_col: str, param: Optional[float] = None
    ) -> pd.DataFrame:
        """Apply 88 treatment"""
        output = deepcopy(ind_df)
        output[ind_col] = np.where(
            output[ind_col] == IndeterminateFormsMapOutput.V_88888888.value,
            param,
            output[ind_col].to_numpy(),
        )
        return output[ind_col].to_numpy()

    @staticmethod
    def apply_v_99999999_substitution(
        ind_df: pd.DataFrame, ind_col: str, subst_value: float
    ) -> pd.DataFrame:
        output = deepcopy(ind_df)
        output[ind_col] = np.where(
            output[ind_col] == IndeterminateFormsMapOutput.V_99999999.value,
            subst_value,
            output[ind_col].to_numpy(),
        )
        return output[ind_col].to_numpy()
