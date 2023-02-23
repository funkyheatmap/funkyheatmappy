import numpy as np
import pandas as pd


def score_to_funkyrectangle(xmin, xmax, ymin, ymax, value, midpoint=0.5, name=None):
    if pd.isna(value):
        return None
    trans = value / midpoint / 2
    x = xmin / 2 + xmax / 2
    y = ymin / 2 + ymax / 2
    r = (trans * 0.9 + 0.1) * min(xmax - xmin, ymax - ymin)
    start = 0
    end = 2 * np.pi
    out = pd.DataFrame({"x": x, "y": y, "r": r, "start": start, "end": end}, index=[0])
    return out.assign(name=name, value=value)
