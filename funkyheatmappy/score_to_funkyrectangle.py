import numpy as np
import pandas as pd


def score_to_funkyrectangle(xmin, xmax, ymin, ymax, size_value, color_value = np.nan, midpoint=0.5, name=None):
    if pd.isna(size_value):
        return None

    if size_value >= midpoint:
        trans = (size_value - midpoint) / (1 - midpoint) / 2 + 0.5
        x = xmin / 2 + xmax / 2
        y = ymin / 2 + ymax / 2
        w = xmax - xmin
        h = ymax - ymin
        corner_size = (0.9 - 0.8 * trans) * min(xmax - xmin, ymax - ymin)
        out = pd.DataFrame(
            {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax, "corner_size": corner_size}, index=[0]
        )
    else:
        trans = size_value / midpoint / 2
        start = 0
        end = 2 * np.pi
        x = xmin / 2 + xmax / 2
        y = ymin / 2 + ymax / 2
        r = (trans * 0.9 + 0.1) * min(xmax - xmin, ymax - ymin)

        out = pd.DataFrame(
            {"x": x, "y": y, "r": r, "start": start, "end": end}, index=[0]
        )

    return out.assign(name=name, size_value=size_value, color_value=color_value)
