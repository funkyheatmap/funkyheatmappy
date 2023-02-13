from numpy import nan, isnan
import pandas as pd


def verify_row_info(data, row_info=None):
    if row_info is None:
        row_info = pd.DataFrame(data.columns, columns=["id"])

    assert isinstance(row_info, pd.DataFrame), "row_info must be a pandas dataframe"
    assert "id" in row_info.columns, "row_info must have a column named 'id'"
    assert all(
        row_info["id"].isin(data.columns)
    ), "row_info must have the same ids as data"
    assert all(
        isinstance(s, str) for s in row_info["id"]
    ), "row_info must have string ids"

    # checkling group
    if "group" not in row_info.columns:
        row_info["group"] = nan

    assert all(
        isinstance(s, str) or isnan(s) for s in row_info["group"]
    ), "row_info must have string groups"

    return row_info
