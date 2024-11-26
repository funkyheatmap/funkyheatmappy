import numpy as np
import pandas as pd


def score_to_funkyrectangle(xmin, xmax, ymin, ymax, value, midpoint=0.5, name=None):
    if pd.isna(value):
        return None

    if value >= midpoint:
        trans = (value - midpoint) / (1 - midpoint) / 2 + 0.5
        corner_size = (0.9 - 0.8 * trans) * min(xmax - xmin, ymax - ymin)
        out = pd.DataFrame(
            {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax, "corner_size": corner_size}, index=[0]
        )
    else:
        trans = value / midpoint / 2
        start = 0
        end = 2 * np.pi
        x = xmin / 2 + xmax / 2
        y = ymin / 2 + ymax / 2
        r = (trans * 0.9 + 0.1) * min(xmax - xmin, ymax - ymin)

        out = pd.DataFrame(
            {"x": x, "y": y, "r": r, "start": start, "end": end}, index=[0]
        )

    return out.assign(name=name, value=value)
