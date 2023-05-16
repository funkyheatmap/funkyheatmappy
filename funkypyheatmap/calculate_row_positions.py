import pandas as pd
import numpy as np


def calculate_row_positions(row_info, row_height, row_space):
    row_pos = pd.DataFrame(row_info).copy()
    row_pos["group_i"] = row_pos.groupby("group").cumcount()
    row_pos["row_i"] = range(len(row_pos))
    row_pos["color_background"] = row_pos["group_i"] % 2 == 0
    row_pos["do_spacing"] = row_pos.groupby("group").ngroup().diff() != 0
    row_pos.loc[row_pos.index[0], "do_spacing"] = False
    row_pos["ysep"] = [
        row_height + 2 * row_space if spacing else row_space
        for spacing in row_pos["do_spacing"]
    ]
    row_pos["y"] = -1 * (
        np.add(
            (row_pos["row_i"] + 1).tolist() * row_height,
            row_pos["ysep"].cumsum().tolist(),
        )
    )
    row_pos["ymin"] = row_pos["y"] - row_height / 2
    row_pos["ymax"] = row_pos["y"] + row_height / 2
    row_pos["height"] = row_height + row_space

    return row_pos
