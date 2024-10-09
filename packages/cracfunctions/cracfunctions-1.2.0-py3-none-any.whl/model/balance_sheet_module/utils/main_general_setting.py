from dataclasses import dataclass
from model.balance_sheet_module.utils.indeterminate_forms import (
    IndeterminateFormsMapOutput,
)
from typing import Tuple, List, Optional, Dict, Union
from pathlib import Path


@dataclass
class MainGeneralSetting:
    # General setting
    project: str
    big_query_dataset: str

    # Indeterminate forms
    indicator_keys: List
    list_indeterminate_forms: Optional[IndeterminateFormsMapOutput] = (None,)

    # Indicator
    big_query_indicator_table_name: Optional[str] = None
    big_query_long_list: Optional[str] = None

    # Ushape
    u_shape_threshold: Optional[float] = None
    u_shape_treatment_bucket: Optional[List[Tuple]] = None
    big_query_ushape_table_name: Optional[str] = None
    big_query_long_list_after_ushape_table_name: Optional[str] = None

    # 88 Treatment
    treatment_88_bucket: Optional[List[Tuple]] = None
    big_query_88_treatment_table_name: Optional[str] = None
    big_query_long_list_after_88_table_name: Optional[str] = None

    # Univariate
    univ_list_analysis: Optional[List] = None
    univ_list_analysis_short_list: Optional[List] = None
    univ_short_list_expert: Optional[List] = None
    univ_perim_table: Optional[str] = None
    univ_long_list_table: Optional[str] = None
    univ_long_list_final_table: Optional[str] = None
    univ_error_percentage: Optional[float] = None
    univ_indeterminate_forms_percentage: Optional[float] = None
    univ_zero_percentage: Optional[float] = None
    univ_conf_interval_ar_area: Optional[float] = None
    univ_other_input: Optional[Dict[str, Optional[float]]] = None
    univ_report_path: Optional[Path] = None

    # Correlation
    correlation_threshold: Optional[float] = None
    correlation_threshold_accuracy: Optional[float] = None
    multicollinearity_threshold: Optional[Union[int, float]] = None
    big_query_long_list_post_corr_intra_table: Optional[str] = None
    big_query_long_list_post_corr_cross_table: Optional[str] = None

    # Logistic transformation
    logistic_t_cutoff_multiplier: Optional[float] = None
    logistic_t_slope_num: Optional[float] = None
    logistic_t_standard_deviation_target: Optional[float] = None
    logistic_t_big_query_perim: Optional[str] = None
    logistic_t_big_query_long_list: Optional[str] = None
    logistic_significance_level: Optional[float] = None

    # Combinatorial
    combinatorial_min_n_variable: Optional[int] = None
    combinatorial_max_n_variable: Optional[int] = None
    combinatorial_criteria: Optional[Dict] = None
    combinatorial_initial_models: Optional[str] = None
    combinatorial_n_batch: Optional[int] = None
    combinatorial_final_model: Optional[str] = None

    # Bootstrapping
    bootstrapping_grouping_variables: Optional[List[str]] = None
    bootstrapping_target_percentage: Optional[float] = None
    bootstrapping_n_iteration: Optional[int] = None
    bootstrapping_biquery_model_beta_out: Optional[str] = None
