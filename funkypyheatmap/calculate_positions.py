import pandas as pd
import numpy as np
from funkypyheatmap.score_to_funkyrectangle import score_to_funkyrectangle
from funkypyheatmap.add_column_if_missing import add_column_if_missing
from funkypyheatmap.calculate_row_positions import calculate_row_positions
from funkypyheatmap.calculate_column_positions import calculate_column_positions

# from funkypyheatmap.plot_funkyrect import plot_funkyrect
from funkypyheatmap.make_data_processor import make_data_processor


def calculate_positions(
    data,
    column_info,
    row_info,
    column_groups,
    row_groups,
    palettes,
    scale_column,
    add_abc,
    col_annot_offset,
    col_annot_angle,
    removed_entries,
):
    row_height = 1
    row_space = 0.1
    row_bigspace = 0.5
    col_width = 1
    col_space = 0.1
    col_bigspace = 0.5

    # Determine row positions
    if not "group" in row_info.columns or all(pd.isna(row_info["group"])):
        row_info["group"] = ""
        row_groups = pd.DataFrame({"group": [""]})
        plot_row_annotation = False
    else:
        plot_row_annotation = True

    row_pos = calculate_row_positions(
        row_info=row_info, row_height=row_height, row_space=row_space
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

    # segment_data = None
    def circle_fun(dat):
        dat = dat.assign(x0=dat["x"], y0=dat["y"], r=row_height / 2 * dat["value"])
        return dat

    circle_data = data_processor("circle", circle_fun)

    def rect_fun(dat):
        return dat

    rect_data = data_processor("rect", rect_fun)

    def funkyrect_fun(dat):
        dat = dat[["xmin", "xmax", "ymin", "ymax", "value"]]
        result = pd.DataFrame()
        for _, row in dat.iterrows():
            column_funkyrect = score_to_funkyrectangle(
                xmin=row["xmin"],
                xmax=row["xmax"],
                ymin=row["ymin"],
                ymax=row["ymax"],
                value=row["value"],
                midpoint=0.8,
            )
            result = pd.concat([result, column_funkyrect])
        return result

    funkyrect_data = data_processor("funkyrect", funkyrect_fun)

    def bar_fun(dat):
        dat = add_column_if_missing(dat, hjust=0)
        dat = dat.assign(
            xmin=dat["xmin"] + (1 - dat["value"]) * dat["xwidth"] * data["hjust"],
            xmax=dat["xmax"] + (1 - dat["value"]) * dat["xwidth"] * (1 - data["hjust"]),
        )
        return dat

    bar_data = data_processor("bar", bar_fun)

    def extract_columns(dat, col_id):
        grouped = dat.groupby(col_id).nth(0).reset_index()
        selected_cols = pd.melt(
            grouped,
            id_vars=[col_id],
            value_vars=["xmin", "xmax"],
            var_name="col",
            value_name="x",
        )
        selected_cols["xend"] = selected_cols["x"]
        return selected_cols[["x", "xend"]]

    def barguides_fun(dat):
        dat = pd.concat(
            [extract_columns(dat, "column_id"), row_pos[["ymin", "ymax"]]], axis=1
        ).assign(palette=np.nan, value=np.nan)
        return dat

    barguides_data = data_processor("bar", barguides_fun)

    def text_fun(dat):
        dat = dat.assign(color="black")
        return dat

    """segment_data = pd.concat(
        [
            segment_data,
            barguides_data.assign(colour="black", size=0.5, linetype="dashed"),
        ],
        ignore_index=True,
    )"""

    text_data = data_processor("text", text_fun)

    def pie_fun(dat):
        value_col = dat[["value"]].reset_index().rename(columns={"index": "iii"})
        value_col["iii"] = value_col["iii"] + 1
        joined_data = dat.merge(value_col, on="iii").drop("iii", axis=1)
        grouped_data = joined_data.groupby(["row_id", "column_id"]).apply(
            lambda group: group.assign(
                y0=group["y"],
                x0=group["x"],
                pct=group["value"].apply(lambda x: x if np.isfinite(x) else 0),
                rad=group["pct"] / group["pct"].sum() * 2 * np.pi,
                rad_end=group["pct"].cumsum() / group["pct"].sum() * 2 * np.pi,
                rad_start=group["pct"].cumsum() / group["pct"].sum() * 2 * np.pi
                - group["rad"],
                r0=0,
                r=row_height / 2,
                value=group["name"],
            )
        )
        filtered_data = grouped_data[
            grouped_data["rad_end"] != grouped_data["rad_start"]
        ]
        filtered_data = filtered_data[filtered_data["pct"] >= 1e-10]
        return filtered_data.reset_index(drop=True)

    pie_data = data_processor("pie", pie_fun)

    return (
        row_pos,
        column_pos,
        # segment_data,
        rect_data,
        circle_data,
        funkyrect_data,
        pie_data,
        text_data,
        # bounds,
        # viz_params,
    )
