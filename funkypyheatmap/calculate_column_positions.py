import pandas as pd
import numpy as np


def calculate_column_positions(column_info, col_space, col_bigspace):
    column_pos = pd.DataFrame(column_info)
    column_pos["do_spacing"] = pd.get_dummies(column_info["group"]).diff() != 0
    column_pos["do_spacing"].iloc[0] = False
    column_pos["xsep"] = np.nan
    column_pos[column_pos["overlay"]]["xsep"] = pd.concat(
        [pd.Series([0]), -1 * column_pos["width"][:-1]]
    )
    column_pos[column_pos["do_spacing"]]["xsep"] = col_bigspace
    column_pos["xsep"] = column_pos["xsep"].fillna(col_space)
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
