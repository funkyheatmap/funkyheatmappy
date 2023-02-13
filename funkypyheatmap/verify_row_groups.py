import pandas as pd


def verify_row_groups(row_info, row_groups=None):
    if row_groups is None and not all(pd.isna(row_info["group"])):
        row_groups = pd.DataFrame(
            {"group": row_info.loc[pd.notnull(row_info["group"]), "group"].unique()}
        )

    if row_groups is None:
        return None
    assert isinstance(row_groups, pd.DataFrame), "row_groups must be a pandas dataframe"
    assert "group" in row_groups.columns, "row_groups must have a column named 'group'"
    assert all(
        isinstance(s, str) for s in row_groups["group"]
    ), "row_groups must have string groups"
    assert all(pd.isna(row_info["group"])) or all(
        row_info["group"].isin(row_groups["group"])
    ), "row_info must have the same groups as row_groups"

    # checking other columns
    row_group_colnames = set(row_groups.columns).difference(set("group", "palette"))

    if len(row_group_colnames) == 0:
        row_groups["level1"] = str(row_groups["group"]).title()

    for colname in row_group_colnames:
        assert all(isinstance(s, str) for s in row_groups[colname]), (
            "row_groups must have string " + colname + "s"
        )

    return row_groups
