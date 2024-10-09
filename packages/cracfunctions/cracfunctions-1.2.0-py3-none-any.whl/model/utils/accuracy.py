import numpy as np
import plotly.graph_objects as go
from pathlib import Path
from dataclasses import dataclass
from sklearn.metrics import roc_auc_score, roc_curve
import pandas as pd
import os
import matplotlib.pyplot as plt


@dataclass
class GiniOutput:
    """Gini standard output"""

    lc_true: np.ndarray
    lc_pred: np.ndarray
    gini: float


class AccuracyEngine:
    """Accuracy engine"""

    def compute_gini(
        self,
        x: np.ndarray,
        y: np.ndarray,
    ) -> GiniOutput:
        """Calculate accuracy - Gini methodology"""
        # Check dimension
        assert x.shape == y.shape, "x and y must have the same dimensions"
        assert x.ndim == 1, "only 1d arrays are allowed"

        # True and predicted order
        z = np.column_stack((y, x))
        true_order = z[z[:, 0].argsort()][::-1, 0]
        pred_order = z[z[:, 1].argsort()][::-1, 0]

        # Compute Lorenz curves
        lorenz_curves_true = np.cumsum(true_order) / np.sum(true_order)
        lorenz_curves_pred = np.cumsum(pred_order) / np.sum(pred_order)

        # Compute areas
        perc_tot_def = y.sum() / y.shape[0]
        area_true = (1 - perc_tot_def) + perc_tot_def * 0.5
        area_pred = np.trapz(lorenz_curves_pred, dx=1 / lorenz_curves_pred.shape[0])

        return GiniOutput(
            lc_true=lorenz_curves_true,
            lc_pred=lorenz_curves_pred,
            gini=(area_pred - 0.5) / (area_true - 0.5),
        )

    def chart_gini(
        self,
        gini_output: GiniOutput,
        direction: float,
        path_output: Path = Path(),
    ) -> plt.figure:
        """Compute the graphic representation of the Lorenz curves (Gini)"""
        diagonal = np.linspace(
            1 / gini_output.lc_true.shape[0], 1, gini_output.lc_true.shape[0]
        )
        fig, ax = plt.subplots(figsize=(4, 2.5))
        ax.plot(diagonal, diagonal, label="Random guess")
        if direction == 1:
            ax.plot(gini_output.lc_true, diagonal, label="Perfect model")
        else:
            ax.plot(diagonal, gini_output.lc_true, label="Perfect model")
        ax.plot(diagonal, gini_output.lc_pred, label="CAP curve")

        ax.set(xlabel="% Population", ylabel="% Default")
        ax.legend()
        return fig

    def compute_somersd(
        self,
        x: np.ndarray,
        y: np.ndarray,
    ) -> float:
        """Calculate accuracy - Gini methodology"""
        # Check dimension
        assert x.shape == y.shape, "x and y must have the same dimensions"
        assert x.ndim == 1, "only 1d arrays are allowed"

        # True and predicted order
        z = np.column_stack((y, x))
        z = pd.DataFrame(z, columns=["y", "x"])
        z = z[((z.y.isnull() == False) & (z.x.isnull() == False))]
        z = z[((z.y != np.inf) & (z.x != np.inf))]
        z = z[((z.y != -np.inf) & (z.x != -np.inf))]
        auc = roc_auc_score(z.y.to_list(), z.x.to_list())
        return 2 * auc - 1

    @staticmethod
    def adjust_accuracy_sign(ar: float, sign: int) -> float:
        if sign * ar < 0.0:
            return abs(ar)
        else:
            return -abs(ar)

    def chart_roc_curve(
        self,
        x: np.ndarray,
        y: np.ndarray,
        fl_show: bool = False,
        fl_save: bool = False,
        path_output: Path = Path(),
    ) -> None:
        fpr, tpr, _ = roc_curve(list(y), list(x))
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name="ROC Curve"))
        fig.add_trace(
            go.Scatter(
                x=[0, 1],
                y=[0, 1],
                mode="lines",
                name="Random Guess",
            )
        )

        fig.update_layout(
            title="ROC Curve",
            xaxis=dict(title="False Positive Rate"),
            yaxis=dict(title="True Positive Rate"),
            margin=dict(l=0, r=0, t=0, b=0),
            width=400,  # pixels
            height=300,  # pixels
        )

        if fl_show:
            fig.show()
        if fl_save:
            if not os.path.exists(path_output.parent):
                os.mkdir(path_output.parent)
            fig.write_image(path_output)
        return fig
