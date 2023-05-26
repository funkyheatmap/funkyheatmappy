def position_arguments(
    row_height=1,
    row_space=0.1,
    row_bigspace=0.5,
    col_width=1,
    col_space=0.1,
    col_bigspace=0.5,
    col_annot_offset=3,
    col_annot_angle=30,
    expand_xmin=0,
    expand_xmax=2,
    expand_ymin=0,
    expand_ymax=0,
):
    """
    Defines parameters for positioning in a plot.

    :param row_height: The height of the rows.
    :type row_height: float
    :param row_space: The space between rows.
    :type row_space: float
    :param row_bigspace: The large space between row groups.
    :type row_bigspace: float
    :param col_width: The width of the columns.
    :type col_width: float
    :param col_space: The space between columns.
    :type col_space: float
    :param col_bigspace: The large space between column groups.
    :type col_bigspace: float
    :param col_annot_offset: How much the column annotation will be offset by.
    :type col_annot_offset: float
    :param col_annot_angle: The angle of the column annotation labels.
    :type col_annot_angle: float
    :param expand_xmin: The minimum expansion of the plot in the x direction.
    :type expand_xmin: float
    :param expand_xmax: The maximum expansion of the plot in the x direction.
    :type expand_xmax: float
    :param expand_ymin: The minimum expansion of the plot in the y direction.
    :type expand_ymin: float
    :param expand_ymax: The maximum expansion of the plot in the y direction.
    :type expand_ymax: float
    """
    return {
        "row_height": row_height,
        "row_space": row_space,
        "row_bigspace": row_bigspace,
        "col_width": col_width,
        "col_space": col_space,
        "col_bigspace": col_bigspace,
        "col_annot_offset": col_annot_offset,
        "col_annot_angle": col_annot_angle,
        "expand_xmin": expand_xmin,
        "expand_xmax": expand_xmax,
        "expand_ymin": expand_ymin,
        "expand_ymax": expand_ymax,
    }
