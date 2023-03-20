import pandas as pd
import numpy as np


def calculate_column_positions(column_info, col_space, col_bigspace):
    column_pos = pd.DataFrame(column_info)
    do_spacing = (
        column_info.groupby("group").ngroup().diff(periods=-1).shift(1).fillna(0)
    ).rename("do_spacing")
    column_pos = pd.concat([column_pos, do_spacing != 0], axis=1)

    column_pos["xsep"] = col_space
    overlay_true = column_pos[column_pos["overlay"]]
    column_pos[column_pos["do_spacing"]]["xsep"] = col_bigspace
    column_pos.loc[column_pos["overlay"], "xsep"] = -1 * overlay_true["width"].shift(
        1
    ).fillna(0)

    column_pos["xwidth"] = column_info["width"]
    overlay_true_and_width_neg = column_pos[
        (column_pos["overlay"]) & (column_pos["width"] < 0)
    ]
    column_pos[(column_pos["overlay"]) & (column_pos["width"] < 0)]["xwidth"] = (
        overlay_true_and_width_neg["width"] - overlay_true_and_width_neg["xsep"]
    )
    column_pos[column_pos["overlay"]]["xwidth"] = column_pos[column_pos["overlay"]][
        "xsep"
    ]
    column_pos["xmax"] = (column_pos["xwidth"] + column_pos["xsep"]).cumsum()
    column_pos["xmin"] = column_pos["xmax"] - column_pos["xwidth"]
    column_pos["x"] = column_pos["xmin"] + column_pos["xwidth"] / 2
    return column_pos
