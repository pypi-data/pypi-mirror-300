import pandas as pd
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from copy import deepcopy
from model.utils.percentiles import PercentileEngine, InterpolationType
from model.utils.accuracy import AccuracyEngine
from model.balance_sheet_module.utils.indeterminate_forms import (
    IndeterminateFormsMapOutput,
)
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from jinja2 import Template
from weasyprint import HTML
import numpy as np


class UnivariateEngine:
    @staticmethod
    def univ_stat(
        ind_df: pd.DataFrame,
        long_list: pd.DataFrame,
        default_col: str = "default",
        list_indeterminate_forms: Optional[List[IndeterminateFormsMapOutput]] = None,
        round_digit: int = 9,
    ) -> pd.DataFrame:
        # Indet forms
        if list_indeterminate_forms is not None:
            neg_mln = (
                IndeterminateFormsMapOutput.V_N_100000000
                if IndeterminateFormsMapOutput.V_N_100000000 in list_indeterminate_forms
                else IndeterminateFormsMapOutput.V_N_1000000
            )
            pos_mln = (
                IndeterminateFormsMapOutput.V_P_100000000
                if IndeterminateFormsMapOutput.V_P_100000000 in list_indeterminate_forms
                else IndeterminateFormsMapOutput.V_P_100000000
            )

        long_list_out = deepcopy(long_list)
        long_list_out["min"] = None
        long_list_out["max"] = None
        long_list_out["mean"] = None
        long_list_out["median"] = None
        long_list_out["p_1"] = None
        long_list_out["p_5"] = None
        long_list_out["p_10"] = None
        long_list_out["p_90"] = None
        long_list_out["p_95"] = None
        long_list_out["p_99"] = None
        for ind in range(long_list_out.shape[0]):
            name = long_list_out.loc[ind, "name"]
            perim_no_indet = ind_df[
                (
                    (ind_df[name] != neg_mln.value)
                    & (ind_df[name] != pos_mln.value)
                    & (ind_df[name] != IndeterminateFormsMapOutput.V_99999999.value)
                )
            ]
            percentiles = PercentileEngine(
                interpolation_type=InterpolationType.GE_THRESHOLD
            ).compute_percentile(
                x=perim_no_indet[name].to_numpy(),
                percentile=[0.01, 0.05, 0.10, 0.9, 0.95, 0.99],
            )
            long_list_out.loc[ind, "min"] = round(
                perim_no_indet[name].min(),
                round_digit,
            )
            long_list_out.loc[ind, "max"] = round(
                perim_no_indet[name].max(), round_digit
            )
            long_list_out.loc[ind, "mean"] = round(
                perim_no_indet[name].mean(), round_digit
            )
            long_list_out.loc[ind, "median"] = round(
                perim_no_indet[name].median(), round_digit
            )

            for p_k, p_v in percentiles.items():
                long_list_out.loc[ind, "p_" + str(int(p_k * 1e2))] = round(
                    p_v, round_digit
                )

            if list_indeterminate_forms is not None:
                long_list_out.loc[ind, "perc_indet_forms"] = (
                    ind_df[
                        (
                            (ind_df[name] == neg_mln.value)
                            | (ind_df[name] == pos_mln.value)
                        )
                    ].shape[0]
                    / ind_df.shape[0]
                )
                long_list_out.loc[ind, "perc_errors"] = (
                    ind_df[
                        (ind_df[name] == IndeterminateFormsMapOutput.V_99999999.value)
                    ].shape[0]
                    / ind_df.shape[0]
                )
            long_list_out.loc[ind, "perc_zeros"] = (
                ind_df[(ind_df[name] == 0.0)].shape[0] / ind_df.shape[0]
            )
            long_list_out.loc[ind, "accuracy"] = AccuracyEngine().compute_somersd(
                ind_df[name].to_numpy(),
                ind_df["default"].to_numpy(),
            )
            long_list_out.loc[
                ind, "accuracy_adj_sign"
            ] = AccuracyEngine().adjust_accuracy_sign(
                ar=long_list_out.loc[ind, "accuracy"],
                sign=long_list_out.loc[ind, "direction_after_u_shape_treatment"],
            )

        area_stat = (
            long_list_out[["area", "name", "accuracy_adj_sign"]]
            .groupby(by="area")
            .agg({"name": "count", "accuracy_adj_sign": "mean"})
            .reset_index()
            .rename(columns={"accuracy_adj_sign": "ar_area", "name": "n_area"})
        )
        long_list_out = pd.merge(
            left=long_list_out, right=area_stat, how="left", on=["area"]
        )
        return long_list_out

    @staticmethod
    def extrapolate_univ_stat(
        long_list: pd.DataFrame, ind_col: str, round_digit: int = 4
    ) -> pd.DataFrame:
        out = pd.DataFrame(
            {
                "Area": [
                    long_list.loc[(long_list.name == ind_col), "area"].values[0],
                ],
                "Short list": [
                    long_list.loc[
                        (long_list.name == ind_col), "is_in_short_list"
                    ].values[0]
                ],
                "Direction": [
                    long_list.loc[
                        (long_list.name == ind_col), "direction_after_u_shape_treatment"
                    ].values[0]
                ],
                "AR": [
                    round(
                        long_list.loc[
                            (long_list.name == ind_col), "accuracy_adj_sign"
                        ].values[0],
                        round_digit,
                    )
                ],
                "Ushape": [
                    long_list.loc[(long_list.name == ind_col), "is_u_shape"].values[0]
                ],
                "min": [
                    round(
                        long_list.loc[(long_list.name == ind_col), "min"].values[0],
                        round_digit,
                    )
                ],
                "max": [
                    round(
                        long_list.loc[(long_list.name == ind_col), "max"].values[0],
                        round_digit,
                    )
                ],
                "mean": [
                    round(
                        long_list.loc[(long_list.name == ind_col), "mean"].values[0],
                        round_digit,
                    )
                ],
                "median": [
                    round(
                        long_list.loc[(long_list.name == ind_col), "median"].values[0],
                        round_digit,
                    )
                ],
                "p_1": [
                    round(
                        long_list.loc[(long_list.name == ind_col), "p_1"].values[0],
                        round_digit,
                    )
                ],
                "p_90": [
                    round(
                        long_list.loc[(long_list.name == ind_col), "p_90"].values[0],
                        round_digit,
                    )
                ],
                "p_95": [
                    round(
                        long_list.loc[(long_list.name == ind_col), "p_95"].values[0],
                        round_digit,
                    )
                ],
                "p_99": [
                    round(
                        long_list.loc[(long_list.name == ind_col), "p_99"].values[0],
                        round_digit,
                    )
                ],
            },
            index=["Stats"],
        ).T

        return out

    @staticmethod
    def create_default_indicator_dist_chart(
        ind_df: pd.DataFrame,
        ind_name: str,
        bins: int = 20,
        default_col: str = "default",
    ) -> plt.figure:
        """Default vs indicator distribution chart for the univariate report"""

        fig, ax1 = plt.subplots(figsize=(6, 4))

        # Filter
        x = ind_df.loc[
            (
                (ind_df[ind_name] >= ind_df[ind_name].quantile(0.05))
                & (ind_df[ind_name] <= ind_df[ind_name].quantile(0.95))
            ),
        ]

        # Create histogram
        ax1.hist(x[ind_name], bins=bins, density=True, alpha=0.7, label=ind_name)
        ax1.set_xlabel(x[ind_name])
        ax1.set_ylabel("% Distribution")
        ax1.set_title("Indicator distribution vs Default rate")

        # Calculate default rate
        _, bin_edges = np.histogram(x[ind_name], bins=bins)
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
        default_rate = [
            ind_df.loc[
                (
                    (ind_df[ind_name] >= bin_edges[i - 1])
                    & (ind_df[ind_name] < bin_edges[i])
                ),
                default_col,
            ].sum()
            / ind_df.shape[0]
            for i in range(1, bin_edges.shape[0])
        ]

        # Create default rate line plot on secondary y-axis
        ax2 = ax1.twinx()
        ax2.plot(bin_centers, default_rate, "ro-", label="Default rate")
        ax2.set_ylabel("Default rate")
        ax2.yaxis.set_major_formatter(PercentFormatter(1, decimals=2))

        # Show legend
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        # Combine handles and labels
        combined_handles = handles1 + handles2
        combined_labels = labels1 + labels2

        # Create a single legend
        ax1.legend(combined_handles, combined_labels, loc="upper left")

        return fig

    def univariate_report_input(
        self,
        ind_df: pd.DataFrame,
        long_list: pd.DataFrame,
        ind_col: str,
        default_col: str = "default",
        direction_col: str = "direction_after_u_shape_treatment",
    ) -> Tuple:
        """Inputs calculation for the univariate report"""

        gini_chart = AccuracyEngine().chart_gini(
            gini_output=AccuracyEngine().compute_gini(
                x=ind_df[ind_col],
                y=ind_df[default_col],
            ),
            direction=long_list.loc[(long_list.name == ind_col), direction_col].values[
                0
            ],
        )
        default_chart = self.create_default_indicator_dist_chart(
            ind_df=ind_df, ind_name=ind_col, default_col=default_col
        )
        statistics = self.extrapolate_univ_stat(long_list=long_list, ind_col=ind_col)

        return gini_chart, default_chart, statistics

    def univariate_report(
        self,
        path: Path,
        ind_df: pd.DataFrame,
        long_list: pd.DataFrame,
        analysis_name: str,
        fl_save: bool = False,
        direction_col: str = "direction_after_u_shape_treatment",
    ) -> None:
        # Define your HTML template
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Univariate analysis</title>
            <style>
                .small-text {
                    font-size: 10px;
                }

                .chart-container {
                    max-width: auto;
                    height: auto;
                }
                .chartbelow-container {
                    max-width: auto;
                    height: auto;
                    margin-top: 20px;
                }
                .subtitle {
                    margin-top: 100px; 
                }
                .table-container {
                    max-width: auto;
                    height: auto;
                }
                .bordered-table {
                    border-collapse: collapse; 
                    width: 100%; 
                }

                .bordered-table th,
                .bordered-table td {
                    border: 1px solid #000; 
                    padding: 8px; 
                }
            </style>
        </head>
        <body>
            {% for page_data in pages %}
            <div style="page-break-before: always; text-align: center;">
                <h1>Indicator: {{ page_data['indicator'] }}</h1>

                <div style="display: flex;">
                    <div style="flex: 1;">
                        <div class="small-text">
                            <h2>Descriptive stats</h2>
                            <div class="table-container">
                                <table class="bordered-table">
                                    {{ page_data['table'] | safe }}
                                </table>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1;">
                        <div class="small-text">
                            <h2>CAP curve</h2>
                            <div class="chart-container">
                                <div class="chart" style="width: 70px; height: 50px;">
                                    {{ page_data['ar_chart'] | safe }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="small-text subtitle">
                    <h2>Default rate vs indicator distribution</h2>
                    <div class="chart-container">
                        <div class="chart" style="width: 100px; height: 100px;">
                            {{ page_data['dr_chart'] | safe }}
                        </div>
                    </div>
                </div>

            </div>
            {% endfor %}
        </body>
        </html>
        """

        pages = []
        for ind in range(long_list.shape[0]):
            name = long_list.loc[ind, "name"]
            gini_chart, default_chart, statistics = self.univariate_report_input(
                ind_df=ind_df,
                long_list=long_list,
                ind_col=name,
                direction_col=direction_col,
            )
            pages_data = {}
            pages_data["indicator"] = name
            pages_data["table"] = statistics.to_html(
                classes="table table-bordered", index=True
            )

            # Save chart
            ar_name = "ar_" + analysis_name + "_" + name + ".png"
            dr_name = "dr_" + analysis_name + "_" + name + ".png"
            gini_chart.savefig(path.joinpath("charts").joinpath(ar_name))
            default_chart.savefig(path.joinpath("charts").joinpath(dr_name))
            plt.close()

            # Transform chart to html content
            pages_data["ar_chart"] = f'<img src="{ar_name}">'
            pages_data["dr_chart"] = f'<img src="{dr_name}">'

            pages.append(pages_data)

        # Render the template with the provided data
        base_url = str(path.joinpath("charts"))
        template = Template(template_str)
        rendered_html = template.render(pages=pages)

        if fl_save:
            # Convert HTML to PDF using WeasyPrint
            HTML(string=rendered_html, base_url=base_url).write_pdf(
                path.joinpath("documents").joinpath(
                    "ar_" + analysis_name + "_report_univ.pdf"
                )
            )
