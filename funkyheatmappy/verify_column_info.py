import pandas as pd
import re
import numpy as np
from pandas.api.types import is_string_dtype, is_numeric_dtype, is_dict_like


def verify_column_info(data, column_info=None):
    if column_info is None:
        column_info = pd.DataFrame(index=data.columns)
        column_info.index.names = ["id"]
    if "id" in column_info.columns:
        column_info.index = column_info["id"]
    assert isinstance(
        column_info, pd.DataFrame
    ), "column_info must be a pandas dataframe"
    # assert "id" in column_info.columns, "column_info must have a column named 'id'"
    assert all(
        column_info.index.isin(data.columns)
    ), "column_info must have the same ids as data"
    assert all(
        isinstance(s, str) for s in column_info.index
    ), "column_info must have string ids"

    # checking options
    if "options" in column_info.columns:
        column_info = pd.concat(
            [
                column_info,
                pd.concat(
                    [
                        pd.DataFrame([row], index=[column_info.index[i]])
                        for i, row in enumerate(column_info["options"])
                    ]
                ),
            ],
            axis=1,
        ).drop("options", axis=1)

    # checking name
    if "name" not in column_info.columns:
        column_info["name"] = [re.sub("_", "", s).title() for s in column_info.index]
    column_info["name"] = [ "" if not isinstance(name, str) else name for name in column_info["name"] ]
    assert all(
        isinstance(s, str) for s in column_info["name"]
    ), "column_info must have string names"

    # checking geom
    if "geom" not in column_info.columns:
        for col in data.columns:
            if is_numeric_dtype(data[col]):
                column_info.loc[column_info.index == col, "geom"] = "funkyrect"
            elif is_string_dtype(data[col]):
                column_info.loc[column_info.index == col, "geom"] = "text"
            elif is_dict_like(data[col]):
                column_info.loc[column_info.index == col, "geom"] = "pie"
    assert all(
        column_info["geom"].isin(
            ["funkyrect", "text", "pie", "circle", "rect", "bar", "image"]
        )
    ), "column_info must have a valid geom"
    assert all(
        isinstance(s, str) for s in column_info["geom"]
    ), "column_info must have string geoms"

    # checking group
    if "group" not in column_info.columns:
        column_info["group"] = np.nan
    assert all(
        isinstance(s, str) or pd.isna(s) for s in column_info["group"]
    ), "column_info must have string groups"

    # checking palette
    if "palette" not in column_info.columns:
        column_info["palette"] = "numerical_palette"
        column_info.loc[column_info["geom"] == "pie", "palette"] = "categorical_palette"
        column_info.loc[column_info["geom"] == "text", "palette"] = np.nan
    assert all(
        isinstance(s, str) or np.isnan(s) for s in column_info["palette"]
    ), "column_info must have string palettes"

    # checking width
    if "width" not in column_info.columns:
        column_info["width"] = 1
        column_info.loc[column_info["geom"] == "text", "width"] = 6
        column_info.loc[column_info["geom"] == "bar", "width"] = 4
    assert all(
        isinstance(s, int) or isinstance(s, float) for s in column_info["width"]
    ), "column_info must have numerical widths"
    column_info["width"] = column_info["width"].fillna(1)

    # checking overlay
    if "overlay" not in column_info.columns:
        column_info["overlay"] = False
    column_info.loc[column_info["overlay"].isnull(), "overlay"] = False
    assert all(
        isinstance(s, bool) for s in column_info["overlay"]
    ), "column_info must have boolean overlays"

    # checking legend
    if "legend" not in column_info.columns:
        column_info["legend"] = column_info["geom"] != "text"

    return column_info
