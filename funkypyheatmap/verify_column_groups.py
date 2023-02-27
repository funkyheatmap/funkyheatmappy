import pandas as pd
import numpy as np


def verify_column_groups(column_info, column_groups=None):
    if column_groups is None and not all(pd.isna(column_info["group"])):
        column_groups = pd.DataFrame(
            {
                "group": column_info.loc[
                    pd.notnull(column_info["group"]), "group"
                ].unique()
            }
        )

    if column_groups is None:
        return None
    assert isinstance(
        column_groups, pd.DataFrame
    ), "column_groups must be a pandas dataframe"
    assert (
        "group" in column_groups.columns
    ), "column_groups must have a column named 'group'"
    assert all(
        isinstance(s, str) for s in column_groups["group"]
    ), "column_groups must have string groups"
    assert all(
        (pd.isna(column_info["group"]))
        | (column_info["group"].isin(column_groups["group"]))
    ), "column_info must have the same groups as column_groups"

    if not all(column_groups["group"].isin(column_info["group"])):
        unused = np.unique(
            column_groups["groups"][~column_groups["groups"].isin(column_info["group"])]
        )
        print("The following groups are not used in column_info: " + ", ".join(unused))

    # checking palette
    if "palette" not in column_groups.columns:
        column_groups["palette"] = np.nan
    assert all(
        isinstance(s, str) or pd.isna(s) for s in column_groups["palette"]
    ), "column_groups must have string palettes"

    # checking other columns
    column_group_colnames = set(column_groups.columns).difference({"group", "palette"})

    if len(column_group_colnames) == 0:
        column_groups["level1"] = str(column_groups["group"]).title()

    for colname in column_group_colnames:
        assert all(isinstance(s, str) for s in column_groups[colname]), (
            "column_groups must have string " + colname + "s"
        )

    return column_groups
