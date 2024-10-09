import numpy as np
from typing import List, Union, Dict
from enum import Enum


class InterpolationType(Enum):
    LOWER = "LOWER"
    HIGHER = "HIGHER"
    LINEAR_INTERPOLATION = "LINEAR_INTERPOLATION"
    GE_THRESHOLD = "GE_THRESHOLD"  # SAS


class PercentileEngine:
    def __init__(self, interpolation_type: InterpolationType) -> None:
        self._interpolation_type = interpolation_type

    @property
    def interpolation_type(self) -> InterpolationType:
        return self._interpolation_type

    def update_interpolation_type(self, interpolation_type: InterpolationType) -> None:
        self._interpolation_type = interpolation_type

    @staticmethod
    def _ge_threshold_calc(x: np.ndarray, percentile: float) -> float:
        x = np.sort(x)
        k = int(percentile * (x.shape[0] - 1))
        if (k + 1) / x.shape[0] >= percentile:
            return x[k]
        else:
            return x[k + 1]

    def compute_percentile(
        self, x: np.ndarray, percentile: Union[List, float]
    ) -> Union[Dict[float, float], float]:
        if self._interpolation_type == InterpolationType.GE_THRESHOLD:
            if isinstance(percentile, float):
                return self._ge_threshold_calc(x, percentile)
            else:
                return {p: self._ge_threshold_calc(x, p) for p in percentile}
