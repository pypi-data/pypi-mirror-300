import pandas as pd
from typing import Dict, List, Union
from model.utils.module_type import ModuleType
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class IntegStep:
    intercept: float
    estimates: Dict[Union[ModuleType, int], float]


def main(
    module_dict: Dict[ModuleType, pd.DataFrame],
    score_map: Dict[ModuleType, str],
    integ_step: Dict[int, IntegStep],
) -> Dict[int, pd.DataFrame]:
    """
    Integration method:
        - module_dict: the values of the dictionary represent the dataset of the modules' scores
        - score_map: the values of the dictionary represent the column names of the scores
        - integ_step: steps of the integration. For each key of the dictionary (step of the integration),
                      the value represents the list of modules to be integrated with their associated betas.
                      Differently from module_dict and integ_step, the integ_step can be also integers, since
                      they can represent the output of previous steps
    """
    integ_step_ordered = {k: integ_step[k] for k in sorted(integ_step)}
    out_dict = {k: 0.0 for k in integ_step_ordered.keys()}

    # Setup parameters that must be updated each step
    module_dict_upd = deepcopy(module_dict)
    score_map_upd = deepcopy(score_map)

    # Perform the integration
    for i_step in out_dict.keys():
        out_dict[i_step] = integ_step_ordered[i_step].intercept
        for mod, beta in integ_step_ordered[i_step].estimates.items():
            out_dict[i_step] += module_dict_upd[mod][score_map_upd[mod]].values * beta
        out_dict[i_step] = pd.DataFrame({"step_" + str(i_step): out_dict[i_step]})
        module_dict_upd[i_step] = out_dict[i_step]
        score_map_upd[i_step] = "step_" + str(i_step)

    return out_dict
