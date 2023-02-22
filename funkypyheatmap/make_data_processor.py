import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_string_dtype
from funkypyheatmap.add_column_if_missing import add_column_if_missing


def make_data_processor(data, column_pos, row_pos, scale_column, palette_list):
    # def data_processor(patch_types, fun):
    patch_types = "text"

    def fun(x):
        return x

    column_sels = pd.DataFrame(column_pos)
    column_sels = column_sels[column_sels["geom"].isin([patch_types])]
    column_sels = column_sels.drop(["group", "name", "do_spacing"], axis=1)
    column_sels.index.names = ["column_id"]
    column_sels = add_column_if_missing(column_sels, label=np.nan, scale=True)

    if column_sels.shape[0] == 0:
        return pd.DataFrame()
    result = pd.DataFrame()
    for index, row in column_sels.iterrows():
        row["label"] = (
            index if row["geom"] == "text" and np.isnan(row["label"]) else row["label"]
        )

        # row_sel = pd.DataFrame(row_pos)
        row_sel = row_pos[["ysep", "y", "ymin", "ymax"]]
        row_sel.index.names = ["row_id"]

        # data_sel = pd.DataFrame(data)
        data_sel = data[["id", index]]
        data_sel = data_sel.rename(columns={index: "value", "id": "row_id"})

        labelcolumn_sel = pd.DataFrame() if pd.isna(row["label"]) else row

        if labelcolumn_sel.shape[0] > 0:
            label_sel = (
                data.assign(row_id=data["id"])
                .filter(["row_id", labelcolumn_sel["label"]])
                .melt(
                    id_vars="row_id", var_name="label_column", value_name="label_value"
                )
            )
            labelcolumn_to_merge = pd.DataFrame(
                [
                    {
                        "label_column": labelcolumn_sel["label"],
                        "column_id": labelcolumn_sel.name,
                    }
                    for _ in range(label_sel.shape[0])
                ]
            )
            label_sel = label_sel.merge(
                labelcolumn_to_merge, on="label_column", how="left"
            ).drop(columns="label_column")
            data_sel = data_sel.merge(label_sel, on=["row_id", "column_id"], how="left")

        dat = data_sel.join(row_sel)
        dat = dat.join(
            pd.DataFrame(
                [
                    pd.concat([pd.Series({"column_id": index}), row])
                    for _ in range(dat.shape[0])
                ],
                index=dat.index,
            )
        )

        if scale_column & row["scale"] & is_numeric_dtype(dat["value"]):
            dat["value"] = dat.groupby("column_id")["value"].transform(
                lambda x: (x - x.min()) / (x.max() - x.min())
            )

        dat = fun(dat)

        # determine colours

        if pd.notna(row["palette"]):
            palette_sel = palette_list[row["palette"]]
            if is_string_dtype(dat["value"]):
                dat["col_value"] = dat["value"]
            elif is_numeric_dtype(dat["value"]):
                dat["col_value"] = (dat["value"] * (len(palette_sel) - 1)).round(
                    decimals=0
                ) + 1
            else:
                dat["col_value"] = np.nan

            dat["colour"] = palette_sel
            """[
            "#444444FF" if np.isnan(col_val) else palette_sel[col_val] for col_val in dat["col_value"]
            ]"""
            dat = dat.drop(["col_value", "value"], axis=1)
        result = pd.concact([result, dat])
    return result

    # return data_processor
