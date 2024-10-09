import pandas as pd
from typing import Optional, Dict
from model.balance_sheet_module.utils.indeterminate_forms import (
    IndeterminateFormsEngine,
    IndeterminateFormsMapOutput,
    IndeterminateForms,
)


from copy import deepcopy
import re
from enum import Enum
import numpy as np



class IndicatorType(Enum):
    RATIO = "R"
    LOG = "L"
    FITCH = "F"


class IndicatorCalcEngine:
    def __init__(
        self,
        name: str,
        numerator_formula: str,
        denominator_formula: str,
        indicator_type: IndicatorType = IndicatorType.RATIO,
        keys: str = [
            "cod_sndg",
            "cod_fisc",
            "perf_year",
            "anno_bil",
            "area_geo",
            "default",
        ],
    ) -> None:
        self._name = name
        self._numerator_formula = numerator_formula
        self._denominator_formula = denominator_formula
        self._indicator_type = indicator_type
        self._keys = keys

    @property
    def name(
        self,
    ) -> str:
        return self._name

    @property
    def numerator_formula(
        self,
    ) -> str:
        return self._numerator_formula

    @property
    def denominator_formula(
        self,
    ) -> str:
        return self._denominator_formula

    @property
    def indicator_type(
        self,
    ) -> str:
        return self._indicator_type

    @property
    def keys(
        self,
    ) -> str:
        return self._keys

    @staticmethod
    def _is_float(string: str) -> bool:
        try:
            float(string)
            return True
        except ValueError:
            return False

    def _convert_str(
        self, initial_string: str, operators: str = r"[\-\+\*\(\)\/]"
    ) -> str:
        non_operators = re.split(operators, initial_string)
        non_operators = [x.strip() for x in non_operators if x]
        non_operators = [
            v
            if v in ["abs", ""] or self._is_float(v)
            else ("log" if v in ["log", "Log"] else "input_df['" + v + "']")
            for v in non_operators
        ]
        matches = re.findall(operators, initial_string)
        if len(matches) == 0:
            result = non_operators
        elif matches[0] == initial_string[0]:
            result = [x + y for x, y in zip(matches, non_operators)]
        else:
            result = [x + y for x, y in zip(non_operators, matches)]

        if len(matches) > 0:
            if len(matches) > len(non_operators):
                dist = int(len(matches) - len(non_operators))
                for i in range(dist):
                    result.append(matches[-dist + i])
            elif len(matches) < len(non_operators):
                dist = int(len(non_operators) - len(matches))
                for i in range(dist):
                    result.append(list(non_operators)[-dist + i])
            else:
                ...
        final_string = ""
        for i in result:
            final_string += i
        return final_string

    @staticmethod
    def _convert_pandas_str(initial_string: str) -> str:
        return initial_string.replace("Log", "log")

    def compute_indicator_df(
        self,
        input_df: pd.DataFrame,
        indeterminate_forms_map: Dict[IndeterminateForms, Optional[float]],
        round_digit: int = 16,
    ) -> pd.DataFrame:
        output = deepcopy(input_df)
        num = round(
            input_df.eval(
                self._convert_pandas_str(initial_string=self._numerator_formula)
            ),
            round_digit,
        )
        if self._indicator_type == IndicatorType.RATIO:
            den = round(
                input_df.eval(
                    self._convert_pandas_str(initial_string=self._denominator_formula)
                ),
                round_digit,
            )
            output[self._name] = IndeterminateFormsEngine().apply_map(
                num.to_numpy(), den.to_numpy(), indeterminate_forms_map
            )
        elif self._indicator_type == IndicatorType.LOG:
            den = round(
                input_df.eval(
                    self._convert_pandas_str(initial_string=self._denominator_formula)
                ),
                round_digit,
            )
            output[self._name] = np.where(
                den <= 0, IndeterminateFormsMapOutput.V_99999999.value, num
            )
        elif self._indicator_type == IndicatorType.FITCH:
            output[self._name] = round(num / 100.0, round_digit)
        return output[self._keys + [self._name]]
