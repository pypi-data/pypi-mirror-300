import pandas as pd
from typing import List, Tuple
from enum import Enum
from scipy import optimize
from functools import partial


class RootFindingMethod(Enum):
    """Type of root finding method"""

    NEWTON = partial(optimize.newton)
    BRENT = partial(optimize.brentq)


class RootFinding:
    """Class designed to solve root finding problems on pandas.DataFrame"""

    def __init__(
        self,
        optimize_function: callable,
        optimize_method: RootFindingMethod,
        target_var: str,
        arguments: List[str],
        tolerance: float,
        max_iterations: int = None,
        interval: Tuple[int, int] = None,
        derivative_function: callable = None,
    ) -> None:

        self._optimize_function = optimize_function
        self._optimize_method = optimize_method
        self._target_var = target_var
        self._arguments = arguments
        self._tolerance = tolerance
        self._max_iterations = max_iterations
        self._derivative_function = derivative_function

    @property
    def optimize_function(self) -> callable:
        return self._optimize_function

    @property
    def optimize_method(self) -> RootFindingMethod:
        return self._optimize_method

    def evaluate_funciton(self, target_var: float, *args: float) -> float:
        return self._optimize_function(target_var, *args)

    def find_root(self, df_of_variables: pd.DataFrame, target_var: str):
        if self._optimize_method == RootFindingMethod.NEWTON:
            df_of_variables.loc[:, target_var] = df_of_variables.apply(
                lambda row: self._optimize_method.value(
                    self._optimize_function,
                    row[target_var],
                    args=tuple(row.drop(target_var)),
                    tol=self._tolerance,
                    disp=False,
                ),
                axis=1,
            )
            return df_of_variables
        else:
            ...
            raise NotImplementedError(f"{self._optimize_method} has not been implemented yet.")


# non so quanto sia generale... non tutti i metodi hanno gli stessi argomenti! magari per un altro metodo non va bene self._optimize_method.value(....) fatto cosi
# quindi ho messo degli if
# ma allora a sto punto non ha senso definire la funzione da usare nella classe Enum (usando partial) -> si può fare direttamente in find_root
