import numpy as np
import pandas as pd


def verify_row_info(data, row_info=None):
    if row_info is None:
        row_info = pd.DataFrame(index=data.index)

    assert isinstance(row_info, pd.DataFrame), "row_info must be a pandas dataframe"
    # assert "id" in row_info.columns, "row_info must have a column named 'id'"
    assert set(row_info.index) == set(
        data.index
    ), "row_info must have the same index as data"
    assert all(
        isinstance(s, str) for s in row_info.index
    ), "row_info must have string ids"

    # checkling group
    if "group" not in row_info.columns:
        row_info["group"] = np.nan

    assert all(
        isinstance(s, str) or np.isnan(s) for s in row_info["group"]
    ), "row_info must have string groups"

    return row_info
