from dataclasses import dataclass
from typing import List, Optional, Dict
from string import Template


@dataclass
class MainGeneralSetting:
    # General setting
    project: str
    big_query_dataset: str

    # Keys
    col_key: List[str]

    # Process and aggregate questions
    qq_list: List
    default_col_name: str
    ordering_map: Dict[str, Dict[str, int]]
    aggregation_list: Optional[List] = None
    bigquery_table_perim_processed: Optional[str] = None

    # Univariate analysis
    woe_min_den_value: Optional[float] = None
    treat_missing_values: Optional[bool] = None
    mapping_missing_values: Optional[Dict[str, str]] = None
    bigquery_table_univ_report: Optional[str] = None
    bigquery_table_df_woe: Optional[str] = None

    # Correlation analysis
    big_query_corr_pearson_output_table: Optional[str] = None
    big_query_corr_spearman_output_table: Optional[str] = None

    # Area
    area_ind: Optional[Dict[str, List[str]]] = None

    # Multivariate
    multiv_pvalues_threshold: Optional[float] = None
    big_query_multiv_scores: Optional[str] = None
    big_query_multiv_models: Optional[str] = None

    # Bootstrapping
    bootstrapping_grouping_variables: Optional[List[str]] = None
    bootstrapping_n_iter: Optional[int] = None
    bootstrapping_target_percentage: Optional[float] = None
    bootstrapping_biquery_model_beta_out: Optional[str] = None
    bootstrapping_seed: Optional[int] = None
    bootstrapping_biquery_final_scores: Optional[str] = None

    # Final bucket
    n_bucket: Optional[int] = None
    score_unit_interval: Optional[int] = None
    t_test_threshold: Optional[float] = None
    hhi_map: Optional[Dict[str, Template]] = None
    big_query_bucket: Optional[str] = None
    big_query_final_bucket_score: Optional[str] = None
