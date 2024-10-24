import pandas as pd
import numpy as np
import re
from funkyheatmappy.score_to_funkyrectangle import score_to_funkyrectangle
from funkyheatmappy.add_column_if_missing import add_column_if_missing
from funkyheatmappy.calculate_row_positions import calculate_row_positions
from funkyheatmappy.calculate_column_positions import calculate_column_positions
from funkyheatmappy.verify_palettes import default_palettes
from funkyheatmappy.make_data_processor import make_data_processor


def calculate_positions(
    data,
    column_info,
    row_info,
    column_groups,
    row_groups,
    palettes,
    position_args,
    scale_column,
    add_abc,
):
    row_height = position_args["row_height"]
    row_space = position_args["row_space"]
    row_bigspace = position_args["row_bigspace"]
    col_width = position_args["col_width"]
    col_space = position_args["col_space"]
    col_bigspace = position_args["col_bigspace"]
    col_annot_offset = position_args["col_annot_offset"]
    col_annot_angle = position_args["col_annot_angle"]

    # Determine row positions
    if not "group" in row_info.columns or all(pd.isna(row_info["group"])):
        row_info["group"] = ""
        row_groups = pd.DataFrame({"group": [""]})
        plot_row_annotation = False
    else:
        plot_row_annotation = True

    row_pos = calculate_row_positions(
        row_info=row_info,
        row_height=row_height,
        row_space=row_space,
        row_bigspace=row_bigspace,
    )

    # Determine column positions
    if not "group" in column_info.columns or all(pd.isna(column_info["group"])):
        column_info["group"] = ""
        column_groups = pd.DataFrame({"group": [""]})
        plot_column_annotation = False
    else:
        plot_column_annotation = True

    column_pos = calculate_column_positions(
        column_info=column_info, col_space=col_space, col_bigspace=col_bigspace
    )

    # Process data
    data_processor = make_data_processor(
        data=data,
        column_pos=column_pos,
        row_pos=row_pos,
        scale_column=scale_column,
        palette_list=palettes,
    )

    def circle_fun(dat):
        dat = dat.assign(x0=dat["x"], y0=dat["y"], r=row_height / 2 * dat["value"])
        return dat

    circle_data = data_processor("circle", circle_fun)

    def rect_fun(dat):
        return dat

    rect_data = data_processor("rect", rect_fun)

    def funkyrect_fun(dat):
        result = pd.concat(
            [
                score_to_funkyrectangle(
                    xmin=row["xmin"],
                    xmax=row["xmax"],
                    ymin=row["ymin"],
                    ymax=row["ymax"],
                    value=row["value"],
                    midpoint=0.8,
                )
                for _, row in dat[["xmin", "xmax", "ymin", "ymax", "value"]].iterrows()
            ]
        )
        return result

    funkyrect_data = data_processor("funkyrect", funkyrect_fun)

    def bar_fun(dat):
        dat = add_column_if_missing(dat, hjust=0)
        dat = dat.assign(
            xmin=dat["xmin"] + (1 - dat["value"]) * dat["xwidth"] * dat["hjust"],
            xmax=dat["xmax"] - (1 - dat["value"]) * dat["xwidth"] * (1 - dat["hjust"]),
        )
        return dat

    bar_data = data_processor("bar", bar_fun)

    def barguides_fun(dat):
        dat = ((dat.groupby("column_id").first())[["xmin", "xmax"]]).melt(
            var_name="col", value_name="x"
        )
        dat = dat.assign(xend=dat["x"])[["x", "xend"]]
        cols_to_add = pd.DataFrame({"y": row_pos["ymin"], "yend": row_pos["ymax"]})
        result = (
            pd.merge(dat.assign(key=1), cols_to_add.assign(key=1), on="key")
            .drop("key", axis=1)
            .sort_values(["x", "xend"])
            .reset_index(drop=True)
            .drop_duplicates()
            .assign(palette=np.nan, value=np.nan)
        )
        return result

    segment_data = data_processor("bar", barguides_fun).assign(
        colour="black", size=0.5, linestyle="dashed"
    )

    def text_fun(dat):
        dat = dat.assign(color="black")
        return dat

    text_data = data_processor("text", text_fun)

    def pie_fun(dat):
        result = pd.DataFrame()
        for _, row in dat.iterrows():
            value_df = pd.DataFrame(row["value"], index=["end_angle"]).transpose()
            pctgs = value_df["end_angle"] / value_df["end_angle"].sum()
            value_df = (value_df / value_df.sum()) * 360
            value_df = value_df.cumsum().fillna(0)
            value_df["start_angle"] = value_df["end_angle"].shift(1).fillna(0)
            value_df = value_df.loc[value_df["start_angle"] != value_df["end_angle"], :]

            end_angle = (-1 * value_df["start_angle"] + 90) % 360
            start_angle = (-1 * value_df["end_angle"] + 90) % 360
            value_df["start_angle"], value_df["end_angle"] = start_angle, end_angle

            value_df["height"] = row_height / 2
            value_df["x0"] = row["x"]
            value_df["y0"] = row["y"]
            value_df["row_id"] = row["row_id"]
            value_df["value"] = value_df.index
            value_df["pctgs"] = pctgs
            result = pd.concat([result, value_df])
        result = result.dropna(subset="value", axis=0)
        dat = result.merge(dat.drop("value", axis=1), on=["row_id"], how="left")
        return dat

    pie_data = data_processor("pie", pie_fun)

    def image_fun(dat):
        dat = dat.assign(y0=dat["y"] - row_height, height=row_height, width=row_height)
        return dat

    image_data = data_processor("image", image_fun)

    # Add Annotations
    if plot_row_annotation:
        row_annotation = row_groups.melt(
            id_vars="group", var_name="level", value_name="name"
        ).merge(row_pos[["group", "ymin", "ymax"]], how="left", on="group")

        row_annotation = pd.DataFrame(
            {
                "ymin": row_annotation.groupby("name").apply(lambda x: min(x["ymin"])),
                "ymax": row_annotation.groupby("name").apply(lambda x: max(x["ymax"])),
            }
        )
        row_annotation["y"] = (row_annotation["ymin"] + row_annotation["ymax"]) / 2
        row_annotation["xmin"] = -0.5
        row_annotation["xmax"] = 5
        row_annotation = row_annotation[
            (~pd.isna(row_annotation.index)) & (row_annotation.index != "")
        ]

        text_data_rows = pd.DataFrame(
            {
                "xmin": row_annotation["xmin"],
                "xmax": row_annotation["xmax"],
                "ymin": row_annotation["ymax"] + row_space,
                "label_value": [re.sub("\n", " ", x) for x in row_annotation.index],
                "ha": 0,
                "va": 0.5,
                "fontweight": "bold",
                "ymax": (row_annotation["ymax"] + row_space) + row_height,
            }
        )
        text_data = pd.concat([text_data, text_data_rows])

    if plot_column_annotation:
        col_join = column_groups.melt(
            id_vars=["group", "palette"], var_name="level", value_name="name"
        ).merge(column_pos[["group", "xmin", "xmax"]], how="left", on="group")
        text_pct = 0.9
        level_heights = pd.DataFrame(
            col_join.groupby("level").apply(lambda x: max(x["name"].str.count("\n"))),
            columns=["max_newlines"],
        )
        level_heights["height"] = (level_heights["max_newlines"] + 1) * text_pct + (
            1 - text_pct
        )
        level_heights["levelmatch"] = pd.Series(
            [column_groups.columns.tolist().index(x) for x in level_heights.index],
            index=level_heights.index,
            name="level",
        )
        level_heights = level_heights.sort_values(["levelmatch"], ascending=False)
        level_heights["ysep"] = row_space
        level_heights["ymax"] = (
            col_annot_offset
            + (level_heights["height"] + level_heights["ysep"]).cumsum()
            - level_heights["ysep"]
        )
        level_heights["ymin"] = level_heights["ymax"] - level_heights["height"]
        level_heights["y"] = (level_heights["ymin"] + level_heights["ymax"]) / 2
        palette_mids = {
            x: palettes[x][round(len(palettes[x]) / 2)]
            if isinstance(palettes[x], list)
            else list(palettes[x].values())[round(len(palettes[x]) / 2)]
            for x in palettes.keys()
        }
        max_newlines = (
            col_join.groupby("level")
            .apply(lambda x: x["name"].str.count("\n").max())
            .transpose()
        )
        column_annotation = col_join.merge(
            max_newlines.rename("max_newlines"), on="level", how="left"
        )
        xmin = column_annotation.groupby(
            ["level", "name", "palette"], dropna=False
        ).apply(lambda x: min(x["xmin"]))
        xmax = column_annotation.groupby(
            ["level", "name", "palette"], dropna=False
        ).apply(lambda x: max(x["xmax"]))
        column_annotation = (
            pd.concat(
                [
                    xmin.index.to_frame(),
                    xmin.rename("xmin"),
                    xmax.rename("xmax"),
                    ((xmin + xmax) / 2).rename("x"),
                ],
                axis=1,
            )
        ).reset_index(drop=True)

        column_annotation = column_annotation.merge(
            level_heights, on="level", how="left"
        )
        column_annotation = column_annotation[~pd.isna(column_annotation["name"])]
        column_annotation = column_annotation[
            column_annotation["name"].str.contains("[a-zA-Z]")
        ]
        column_annotation["colour"] = [
            palette_mids[col] for col in column_annotation["palette"]
        ]
        rect_data = pd.concat(
            [
                rect_data,
                pd.DataFrame(
                    {
                        "xmin": column_annotation["xmin"],
                        "xmax": column_annotation["xmax"],
                        "ymin": column_annotation["ymin"],
                        "ymax": column_annotation["ymax"],
                        "colour": column_annotation["colour"],
                        "alpha": [
                            1 if lm == 0 else 0.25
                            for lm in column_annotation["levelmatch"]
                        ],
                        "border": False,
                    }
                ),
            ]
        )
        text_data = pd.concat(
            [
                text_data,
                pd.DataFrame(
                    {
                        "xmin": column_annotation["xmin"] + col_space,
                        "xmax": column_annotation["xmax"] - col_space,
                        "ymin": column_annotation["ymin"],
                        "ymax": column_annotation["ymax"],
                        "va": 0.5,
                        "ha": 0.5,
                        "fontweight": [
                            "bold" if lm == 0 else np.nan
                            for lm in column_annotation["levelmatch"]
                        ],
                        "colour": [
                            "white" if lm == 0 else "black"
                            for lm in column_annotation["levelmatch"]
                        ],
                        "label_value": column_annotation["name"],
                    }
                ),
            ]
        )

        if add_abc:
            alphabet = list(map(chr, range(97, 123)))
            c_a_df = (
                column_annotation[column_annotation["levelmatch"] == 0]
                .sort_values("x")
                .reset_index(drop=True)
            )
            text_data_abc = pd.DataFrame(
                {
                    "xmin": c_a_df["xmin"] + col_space,
                    "xmax": c_a_df["xmax"] - col_space,
                    "ymin": c_a_df["ymin"],
                    "ymax": c_a_df["ymax"],
                    "va": 0.5,
                    "ha": 0,
                    "fontweight": "bold",
                    "colour": "white",
                    "label_value": [alphabet[i] + ")" for i in c_a_df.index],
                }
            )
            text_data = pd.concat([text_data, text_data_abc])

    # Add column names
    df = column_pos[column_pos["name"] != ""]
    if df.shape[0] > 0:
        df_column_segments = pd.DataFrame(
            {"x": df["x"], "xend": df["x"], "y": -0.3, "yend": -0.1, "size": 0.5}
        )
        segment_data = pd.concat([segment_data, df_column_segments])
        df_column_text = pd.DataFrame(
            {
                "xmin": df["xmin"],
                "xmax": df["xmax"],
                "ymin": 0,
                "ymax": col_annot_offset,
                "angle": col_annot_angle,
                "va": 0,
                "ha": 0,
                "label_value": df["name"],
            }
        )
        text_data = pd.concat([text_data, df_column_text])

    # Determine plotting window
    minimum_x = min(
        [
            min(lst, default=np.nan)
            for lst in [
                column_pos["xmin"],
                segment_data["x"],
                segment_data["xend"],
                rect_data["xmin"],
                circle_data["x"] - circle_data["r"],
                funkyrect_data["x"] - funkyrect_data["r"],
                pie_data["xmin"],
                text_data["xmin"],
            ]
        ]
    )

    maximum_x = max(
        [
            max(lst, default=np.nan)
            for lst in [
                column_pos["xmax"],
                segment_data["x"],
                segment_data["xend"],
                rect_data["xmax"],
                circle_data["x"] + circle_data["r"],
                funkyrect_data["x"] + funkyrect_data["r"],
                pie_data["xmax"],
                text_data["xmax"],
            ]
        ]
    )

    minimum_y = min(
        [
            min(lst, default=np.nan)
            for lst in [
                row_pos["ymin"],
                segment_data["y"],
                segment_data["yend"],
                rect_data["ymin"],
                circle_data["y"] - circle_data["r"],
                funkyrect_data["y"] - funkyrect_data["r"],
                pie_data["ymin"],
                text_data["ymin"],
            ]
        ]
    )

    maximum_y = max(
        [
            max(lst, default=np.nan)
            for lst in [
                row_pos["ymax"],
                segment_data["y"],
                segment_data["yend"],
                rect_data["ymax"],
                circle_data["y"] + circle_data["r"],
                funkyrect_data["y"] + funkyrect_data["r"],
                pie_data["ymax"],
                text_data["ymax"],
            ]
        ]
    )

    # # Text legend
    # df_text_legend = column_info[
    #     (column_info["geom"] == "text")
    #     & pd.notna(column_info["legend"])
    #     & (column_info["legend"] != False)
    # ]
    # if df_text_legend.shape[0] > 0:
    #     pr_minimum_x = column_pos.loc[[df_text_legend.index[0]]]["xmin"].min()
    #     legend_vals = pd.DataFrame.from_dict(
    #         df_text_legend["legend"].values[0], orient="columns"
    #     )
    #     legend_vals["legend_vals"] = legend_vals.index
    #     legend_vals = legend_vals.reset_index(drop=True)
    #     pr_labels_df = legend_vals.assign(
    #         lab_x1=pr_minimum_x,
    #         lab_x2=pr_minimum_x + 1,
    #         lab_y=legend_pos - 1 - (legend_vals.index + 1) * row_height * 0.9,
    #     )

    #     pr_text_data = pd.concat(
    #         [
    #             pd.DataFrame(
    #                 {
    #                     "xmin": [pr_minimum_x],
    #                     "xmax": [pr_minimum_x],
    #                     "ymin": [legend_pos - 1.5],
    #                     "ymax": [legend_pos - 0.5],
    #                     "label_value": [df_text_legend["name"].values[0]],
    #                     "ha": 0,
    #                     "va": 1,
    #                     "fontweight": ["bold"],
    #                 }
    #             ),
    #             pd.DataFrame(
    #                 {
    #                     "xmin": pr_labels_df["lab_x1"],
    #                     "xmax": pr_labels_df["lab_x1"],
    #                     "ymin": pr_labels_df["lab_y"],
    #                     "ymax": pr_labels_df["lab_y"],
    #                     "label_value": pr_labels_df["legend_vals"],
    #                     "ha": 0,
    #                     "va": 0,
    #                 }
    #             ),
    #             pd.DataFrame(
    #                 {
    #                     "xmin": pr_labels_df["lab_x2"],
    #                     "xmax": pr_labels_df["lab_x2"],
    #                     "ymin": pr_labels_df["lab_y"],
    #                     "ymax": pr_labels_df["lab_y"],
    #                     "label_value": pr_labels_df["legend"],
    #                     "ha": 0,
    #                     "va": 0,
    #                 }
    #             ),
    #         ]
    #     )
    #     text_data = pd.concat([text_data, pr_text_data])

    # Simplify certain geoms
    if funkyrect_data.shape[0] > 0:
        circle_data = pd.concat(
            [
                circle_data,
                funkyrect_data[
                    ~np.isnan(funkyrect_data["start"])
                    & (funkyrect_data["start"] < 1e-10)
                    & (2 * np.pi - 1e-10 < funkyrect_data["end"])
                ][["x", "y", "r", "colour"]],
            ]
        )
        funkyrect_data = funkyrect_data[
            ~(
                ~np.isnan(funkyrect_data["start"])
                & (funkyrect_data["start"] < 1e-10)
                & (2 * np.pi - 1e-10 < funkyrect_data["end"])
            )
        ]

    rect_data = pd.concat([rect_data, bar_data])
    return {
        "row_pos": row_pos,
        "column_pos": column_pos,
        "segment_data": segment_data,
        "rect_data": rect_data,
        "circle_data": circle_data,
        "funkyrect_data": funkyrect_data,
        "pie_data": pie_data,
        "text_data": text_data,
        "image_data": image_data,
        "bounds": {
            "minimum_x": minimum_x,
            "maximum_x": maximum_x,
            "minimum_y": minimum_y,
            "maximum_y": maximum_y,
        },
        "viz_params": row_space,
    }
