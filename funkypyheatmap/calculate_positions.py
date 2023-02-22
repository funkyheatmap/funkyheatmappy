import pandas as pd
from numpy import nan
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

    # just testing somethings
    # plot_funkyrect(data)

    # Process data

    geom_data_processor = make_data_processor(
        data=data, column_pos=column_pos, row_pos=row_pos, scale_column=scale_column, palette_list=palettes
    )
    print("h")
