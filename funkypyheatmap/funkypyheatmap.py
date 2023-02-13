from .verify_data import verify_data
from .verify_column_info import verify_column_info
from .verify_row_info import verify_row_info
from .verify_column_groups import verify_column_groups
from .verify_row_groups import verify_row_groups
from .verify_palettes import verify_palettes
from .calculate_positions import calculate_positions


def funkyheatmap(
    data,
    column_info=None,
    row_info=None,
    column_groups=None,
    row_groups=None,
    palettes=None,
    scale_column=True,
    add_abc=True,
    col_annot_offset=3,
    col_annot_angle=30,
    removed_entries=None,
    expand={"xmin": 0, "xmax": 2, "ymin": 0, "ymax": 0},
):
    data = verify_data(data)
    column_info = verify_column_info(data=data, column_info=column_info)
    row_info = verify_row_info(data=data, row_info=row_info)
    column_groups = verify_column_groups(
        column_info=column_info, column_groups=column_groups
    )
    row_groups = verify_row_groups(row_info=row_info, row_groups=row_groups)
    palettes = verify_palettes(data=data, column_info=column_info, palettes=palettes)

    positions = calculate_positions(
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
        removed_entries
    )
    """

    compose_plot(coordinates, expand)"""
