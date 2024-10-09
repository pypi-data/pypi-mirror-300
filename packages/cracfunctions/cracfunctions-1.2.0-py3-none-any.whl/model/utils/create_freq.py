import pandas as pd
from pathlib import Path


def freq(
    df: pd.DataFrame,
    vars: list,
    missing: bool,
    save_to_excel: bool = False,
    path: Path = Path(),
    name: str = "freq.xlsx",
):
    """This function replicates the proc freq method in SAS:

    df -> the input dataframe (proc freq data = df) DTYPE: DATAFRAME
    vars = [var1, var2, ..., varN]-> the variables i want to see (tables var1, var2, ..., varN) DTYPE: LIST
    missing -> If i want to see missing values or not DTYPE: BOOLEAN

    ADDITIONAL VARIABLES (related to excel)
    save_to_excel -> to save the df in a .xlsx file (proc export data = wrk_lab.output) DTYPE: BOOLEAN
    path -> the path where i save the excel file (if the boolean is True) DTYPE: PATH
    name -> the name i assign to the df saved as an excel file DTYPE: STRING
    """
    frequency = df[vars].value_counts(dropna=missing)
    frequency.name = "FREQUENCY"
    cumfreq = frequency.cumsum()
    cumfreq.name = "CUMULATIVE FREQUENCY"
    perc = frequency / (cumfreq.values.max()) * 100
    perc.name = "PERCENTUAL"
    cumperc = perc.cumsum()
    cumperc.name = "CUMULATIVE PERCENTUAL"
    final_df = pd.concat([frequency, perc, cumfreq, cumperc], axis=1)
    final_df.reset_index(inplace=True)
    if save_to_excel:
        final_df.to_excel(str(path.joinpath(name + ".xlsx")), index=False)
    return final_df
