import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from scipy.stats import norm
from copy import deepcopy
import pandas as pd
from enum import Enum
from functools import partial



def optimize_function(V: float, E: float, F: float, sigma_v0: float, R: float) -> float:
    return (
        E
        - V * norm.cdf((np.log(V / F) + (float(R) + sigma_v0 * sigma_v0 * 0.5)) / sigma_v0)
        + F
        * np.exp(-R)
        * norm.cdf((np.log(V / F) + (R - sigma_v0 * sigma_v0 * 0.5)) / sigma_v0)
    )


def compute_rv_sigma_mu(df: pd.DataFrame) -> pd.DataFrame:

    df.loc[:, "Rv"] = np.where(
        df["Rv"].notnull(), np.log(df["V"]) - np.log(df["V"].shift(1)), np.nan
    )

    df.loc[:, "sigma_v"] = df.groupby(["CIQ_KEY_ID", "DATE_CAP_START"])["Rv"].transform(
        "std"
    ) * np.sqrt(252)
    df.loc[:, "sigma_v"] = np.where(df["sigma_v"] < 0.01, 0.01, df["sigma_v"])
    df.loc[:, "mu"] = (
        df.groupby(["CIQ_KEY_ID", "DATE_CAP_START"])["Rv"].transform("mean") * 252
    )

    return df


def has_converged(df: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame, bool):

    convergence_status = False

    df.loc[:, "sigma_diff"] = abs(df["sigma_v"] - df["sigma_v0"])
    df.loc[:, "conv"] = np.where(df["sigma_diff"] < 0.001, 1, 0)
    df.loc[:, "num_iter"] = np.where(
        df["conv"] == 0, df["num_iter"] + 1, df["num_iter"]
    )
    df.loc[:, "sigma_v0"] = np.where(df["conv"] == 0, df["sigma_v"], df["sigma_v0"])

    df_to_go = df[df["conv"] == 0]
    df_converged = df[df["conv"] == 1]

    if df_to_go.shape[0] == 0:
        convergence_status = True

    return (df_to_go, df_converged, convergence_status)


def compute_dtd(df: pd.DataFrame) -> pd.DataFrame:

    df.loc[:, "EDF"] = df.apply(
        lambda row: norm.cdf(
            -(
                np.log(row["V"] / row["F"])
                + (row["mu"] - (row["sigma_v"] * row["sigma_v"] * 0.5))
            )
            / row["sigma_v"]
        ),
        axis=1,
    )

    df.loc[:, "DTD"] = (
        np.log(df["V"])
        - np.log(df["F"])
        + (df["mu"] - (df["sigma_v"] * df["sigma_v"] * 0.5))
    ) / df["sigma_v"]

    grouped_df = df.groupby(["CIQ_KEY_ID", "DATE_CAP_START"]).last()
    grouped_df.reset_index(inplace=True)

    return grouped_df