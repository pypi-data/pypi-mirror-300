from model.utils.percentiles import PercentileEngine, InterpolationType
from itertools import combinations
import pandas as pd
import numpy as np
from copy import deepcopy
from model.utils.test_stat import TestStat
from model.utils.accuracy import AccuracyEngine
from string import Template
from typing import Dict
from tqdm import tqdm
from model.utils.check_missing import check_missing


class BucketEngine:
    def __init__(
        self,
        n_bucket: int = 3,
        score_unit_interval: int = 20,
        t_test_threshold: float = 0.05,
        hhi_map: Dict[str, Template] = {
            "green": Template("$hhi<=.2"),
            "yellow": Template("$hhi>.2 and $hhi<=.3"),
            "red": Template("$hhi>.3"),
        },
    ) -> None:
        self._n_bucket = n_bucket
        self._score_unit_interval = score_unit_interval
        self._t_test_threshold = t_test_threshold
        self._hhi_map = hhi_map

    @property
    def n_bucket(
        self,
    ) -> int:
        return self._n_bucket

    @property
    def score_unit_interval(
        self,
    ) -> int:
        return self._score_unit_interval

    @property
    def t_test_threshold(
        self,
    ) -> float:
        return self._t_test_threshold

    @property
    def hhi_map(
        self,
    ) -> Dict[str, Template]:
        return self._hhi_map

    def _init_percentile_method(
        self,
    ) -> PercentileEngine:
        return PercentileEngine(interpolation_type=InterpolationType.GE_THRESHOLD)

    def apply_n_bucket(
        self,
        bucket: pd.DataFrame,
        score: pd.DataFrame,
        bucket_col: str = "cluster",
        score_col: str = "score",
        bucket_output_col: str = "bucket",
        missing_bucket: bool = True,
    ) -> None:
        """
        bucket: parametric table
        score: perimeter containing the score
        woe_col: woe column of the parametric table
        bucket_col: bucket column of the parametric table
        bucket_output_col: column to assign to the mapped bucket into the perimeter dataframe
        score_col: score column of the perimeter dataframe
        """
        if missing_bucket:
            missing_bucket = bucket.loc[
                (check_missing(bucket["min"])) & (check_missing(bucket["max"])),
                bucket_col,
            ].values[0]
            bins = [
                x
                for x in bucket["min"].tolist() + [bucket["max"].iloc[-1]]
                if not np.isnan(x)
            ]
            labels = [x for x in bucket[bucket_col] if x != missing_bucket]

            score[bucket_output_col] = pd.cut(
                score[score_col], bins=bins, labels=labels, right=True
            )

            score[bucket_output_col] = np.where(
                check_missing(score[score_col]), missing_bucket, score[bucket_col]
            )
        else:
            bins = [
                x
                for x in bucket["min"].tolist() + [bucket["max"].iloc[-1]]
                if not np.isnan(x)
            ]
            labels = [x for x in bucket[bucket_col]]

            score[bucket_output_col] = pd.cut(
                score[score_col], bins=bins, labels=labels, right=True
            )

    def apply_n_bucket_and_woe(
        self,
        bucket: pd.DataFrame,
        score: pd.DataFrame,
        woe_col: str = "woe",
        bucket_col: str = "cluster",
        score_col: str = "score",
        missing_bucket: bool = True,
        bucket_output_col: str = "cluster",
        woe_output_col: str = "woe_mapped",
    ) -> None:
        """
        bucket: parametric table
        score: perimeter containing the score
        woe_col: woe column of the parametric table
        bucket_col: bucket column of the parametric table
        score_col: score column of the perimeter dataframe
        bucket_output_col: column to assign to the mapped bucket into the perimeter dataframe
        woe_output_col: column to assign to the mapped woe into the perimeter dataframe
        """
    
        self.apply_n_bucket(
            bucket=bucket,
            score=score,
            bucket_col=bucket_col,
            score_col=score_col,
            bucket_output_col = bucket_output_col,
            missing_bucket=missing_bucket,
        )
        dict_woe = {
            key: value for key, value in zip(bucket[bucket_col], bucket[woe_col])
        }
        score[woe_output_col] = score[bucket_output_col].map(dict_woe).astype(float)

    def estimate_n_bucket(
        self, ind_df: pd.DataFrame, score_col: str, def_col: str = "default"
    ) -> pd.DataFrame:
        percentiles_to_compute = list(
            np.linspace(0.0, 1.0, self.score_unit_interval + 1)
        )
        comb = list(combinations(percentiles_to_compute, self._n_bucket - 1))
        comb_filt = [i for i in comb if i[0] != 0.0 and i[1] != 1.0]
        unit_percentiles = self._init_percentile_method().compute_percentile(
            x=ind_df[score_col].to_numpy(), percentile=percentiles_to_compute
        )

        # Init output
        out = pd.DataFrame()

        for comb_i in tqdm(
            comb_filt,
            desc="Bucket creation: ",
            ascii=True,
        ):
            ind_df_comb = deepcopy(ind_df)
            ind_df_comb[score_col + "_adj"] = ind_df_comb[score_col]
            comb_i_integ = (0.0,) + comb_i + (1.0,)
            for i in range(len(comb_i_integ) - 1):
                limit_inf = unit_percentiles[comb_i_integ[i]]
                limit_sup = unit_percentiles[comb_i_integ[i + 1]]
                if i == 0:
                    ind_df_comb[score_col + "_adj"] = np.where(
                        (ind_df_comb[score_col] >= limit_inf)
                        & (ind_df_comb[score_col] <= limit_sup),
                        i + 1,
                        ind_df_comb[score_col + "_adj"],
                    )
                else:
                    ind_df_comb[score_col + "_adj"] = np.where(
                        (ind_df_comb[score_col] > limit_inf)
                        & (ind_df_comb[score_col] <= limit_sup),
                        i + 1,
                        ind_df_comb[score_col + "_adj"],
                    )
            # Perform tests
            # 1) Monotonicity
            test_monotonicity = TestStat().test_monotonicity_dr(
                ind_df=ind_df_comb, var_col=score_col + "_adj", default_col=def_col
            )
            # 2) T test
            test_t = TestStat().t_test(
                ind_df=ind_df_comb,
                var_col=score_col + "_adj",
                default_col=def_col,
                t_test_threshold=self._t_test_threshold,
            )
            # 3) HHI
            test_hhi = TestStat().test_hhi(
                ind_df=ind_df_comb,
                var_col=score_col + "_adj",
                default_col=def_col,
                hhi_map=self._hhi_map,
            )

            # Compute AR
            ar = AccuracyEngine().compute_somersd(
                x=ind_df_comb[score_col + "_adj"].to_numpy(),
                y=ind_df_comb[def_col].to_numpy(),
            )
            out = pd.concat(
                [
                    out,
                    pd.DataFrame(
                        {
                            "combination": [
                                str([unit_percentiles[i] for i in comb_i_integ])
                            ],
                            "test_monotonicity": [test_monotonicity],
                            "test_t": [test_t],
                            "test_hhi": [test_hhi],
                            "ar": [ar],
                        }
                    ),
                ],
                axis=0,
            )

        out_test_passed = (
            out[((out.test_monotonicity) & (out.test_t) & (out.test_hhi == "green"))]
            .sort_values(by="ar", ascending=False)
            .reset_index(drop=True)
        )

        return out_test_passed