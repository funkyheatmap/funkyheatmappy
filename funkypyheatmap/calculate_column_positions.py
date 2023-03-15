import pandas as pd
import numpy as np


def calculate_column_positions(column_info, col_space, col_bigspace):
    column_pos = pd.DataFrame(column_info)
    do_spacing = column_info.groupby("group").ngroup().diff(periods=-1)[:-1]
    do_spacing[pd.isna(do_spacing)] = 0
    column_pos = column_pos.assign(
        do_spacing=pd.concat([pd.Series(False), do_spacing != 0]).tolist()
    )
    column_pos["do_spacing"].iloc[0] = False
    column_pos["xsep"] = np.nan
    column_pos[column_pos["overlay"]]["xsep"] = pd.concat(
        [pd.Series([0]), -1 * column_pos["width"][:-1]]
    )
    column_pos[column_pos["do_spacing"]]["xsep"] = col_bigspace
    column_pos["xsep"] = column_pos["xsep"].fillna(col_space)

    column_pos.loc[column_pos["do_spacing"], "xsep"] = col_bigspace
    column_pos["width_temp"] = [0] + (column_pos["width"][:-1] * -1).values.tolist()
    column_pos.loc[column_pos["overlay"], "xsep"] = column_pos["width_temp"]

    column_pos["xwidth"] = np.nan
    column_pos[column_pos["overlay"] & column_pos["width"] < 0]["xwidth"] = (
        column_pos["width"] - column_pos["xsep"]
    )
    column_pos[column_pos["overlay"]]["xwidth"] = column_pos["xsep"]
    column_pos["xwidth"] = column_pos["xwidth"].fillna(column_pos["width"])
    column_pos["xmax"] = (column_pos["xwidth"] + column_pos["xsep"]).cumsum()
    column_pos["xmin"] = column_pos["xmax"] - column_pos["xwidth"]
    column_pos["x"] = column_pos["xmin"] + column_pos["xwidth"] / 2

    return column_pos
