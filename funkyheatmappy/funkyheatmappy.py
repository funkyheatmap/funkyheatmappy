from .verify_data import verify_data
from .verify_column_info import verify_column_info
from .verify_row_info import verify_row_info
from .verify_column_groups import verify_column_groups
from .verify_row_groups import verify_row_groups
from .verify_palettes import verify_palettes
from .verify_legends import verify_legends
from .calculate_positions import calculate_positions
from .compose_plot import compose_plot
from .position_arguments import position_arguments
from .create_legends import create_funkyrect_legend, create_rect_legend, create_circle_legend, create_text_legend, create_pie_legend, create_image_legend, create_bar_legend

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def funky_heatmap(
    data,
    column_info=None,
    row_info=None,
    column_groups=None,
    row_groups=None,
    palettes=None,
    legends=None,
    position_args=position_arguments(),
    scale_column=True,
    add_abc=True,
):
    """Generate a funky heatmaps for benchmarks

    :param data: A data frame with items by row and features in the columns.
    Must contain one column named `"id"`.
    :type data: pd.DataFrame
    :param column_info: A data frame describing which columns in `data` to plot.
    This data frame should contain the `"id"` of `"data"`as indices and
    the following columns:
    `"id"` = The corresponding column name in `"data"`,
    `"id_color"` = A column name in `data` to use for the color of the resulting 
    geoms. If `NA`, the `id` column will be used.
    `id_size` = A column name in `data` to use for the size of the resulting 
    geoms. If `NA`, the `id` column will be used.
    `"name"` = A label for the column. If `NA` or `""`, no label will be plotted.
    If this column is missing, `id` will be used to generate the `name` column.,
    `"geom"` = The geom of the column. Must be one of: `"funkyrect"`, `"circle"`,
    `"rect"`, `"bar"`, `"pie"`, `"image"` or `"text"`. For `"text"`, the
    corresponding column in `data` must be a `string`. For `"pie"`, the column
    must be a dictionary. For all other geoms, the column must be `numeric`.,
    `"group"` = The grouping id of each column, must match with
    `column_groups[`"group"`]`. If this column is missing or all values are
    `NA`, columns are assumed not to be grouped.,
    `"palette"` = Which palette to colour the geom by. Each value should have a
    matching value in `palettes[`"palette"`]`,
    `"width"` = Custom width for this column (default: 1),
    `"overlay"` = A boolean whether to overlay this column over the previous
    column. If so, the width of that column will be inherited.,
    `"legend"` =  A boolean whether or not to add a legend for this column.,
    `"ha"` = Horizontal alignment. Must be between [0,1]
    `"va"` = Vertical alignment. Must be between [0,1],
    `"size"` = Size of the label, must be between \[0,1\] (only for `"text"`),
    `"label"` = Which column to use as a label (only for `geom = "text"`),
    `"options"` = A dictionary with any of the options above. Any values in
    this column will be spread across the other columns. This is useful for not
    having to provide a data frame with 1000s of columns.
    :type column_info: pd.DataFrame
    :param row_info: A data frame describing the rows of `data`. This data
    should contain two columns:
    `"id"` = Corresponds to the column `data[`"id"`]`.
    `"group"` = The group of the row.
    If all are `NA`, the rows will not be split up into groups.
    :type row_info: pd.DataFrame
    :param column_groups: A data frame describing of how to group the columns
    in `column_info`. Can consist of the following columns:
    `"group"` = The corresponding group in `column_info$group`.
    `"palette"` (optional) = The palette used to colour the column
    group backgrounds.
    `"level1"`= The label at the highest level.
    `"level2"` (optional) = The label at the middle level.
    `"level3"` (optional) = The label at the lowest level (not recommended).
    :type column_groups: pd.DataFrame
    :param row_groups: A data frame describing of how to group the rows in
    `"row_info"`. Can consist of the following columns:
    `"group"` = The corresponding group in `row_info[`"group"`]`.
    `"level1"`= The label at the highest level.
    `"level2"` (optional) = The label at the middle level.
    `"level3"` (optional) = The label at the lowest level (not recommended).
    :type row_groups: pd.DataFrame
    :param palettes: A dataframe. Each entry in `column_info[`"palette"`]
    should have an entry in this object. If an entry is missing, the type of
    the column will be inferred (categorical or numerical) and one of the
    default palettes will be applied. Alternatively, the name of one of the
    standard palette names can be used:
    `"numerical"`: `"Greys"`, `"Blues"`, `"Reds"`, `"YlOrBr"`, `"Greens"`
    `"categorical"`: `"Set3"`, `"Set1"`, `"Set2"`, `"Dark2"`
    :type palettes: pd.DataFrame
    :param scale_column: Whether or not to apply min-max scaling to each
    numerical column.
    :type scale_column: bool
    :param add_abc: Whether or not to add subfigure labels to the different
    columns groups.
    :type add_abc: bool
    :param col_annot_offset: How much the column annotation will be offset by.
    :type col_annot_offset: float
    :param col_annot_angle: The angle of the column annotation labels.
    :type col_annot_angle: float
    :param expand: A dictionary of directions to expand the plot in with the
    following keys: `"xmin"`, `"xmax"`, `"ymin"`, `"ymax"`.
    :type expand: dict
    """
    data = verify_data(data)
    column_info = verify_column_info(data=data, column_info=column_info)
    row_info = verify_row_info(data=data, row_info=row_info)
    column_groups = verify_column_groups(
        column_info=column_info, column_groups=column_groups
    )
    row_groups = verify_row_groups(row_info=row_info, row_groups=row_groups)
    palettes = verify_palettes(data=data, column_info=column_info, palettes=palettes)
    legends = verify_legends(legends, palettes, column_info, data)

    positions = calculate_positions(
        data,
        column_info,
        row_info,
        column_groups,
        row_groups,
        palettes,
        position_args,
        scale_column,
        add_abc,
    )

    nr_legends = sum([legend["enabled"] for legend in legends])
    heights = [data.shape[0], 1]
    
    # Caculate plot size
    width, height = get_plot_size(positions, position_args)

    # Plot main figure
    fig = plt.figure(layout = "constrained")
    fig.set_size_inches(width, height)
    gs = GridSpec(2, nr_legends, figure=fig, height_ratios=heights)
    ax1 = fig.add_subplot(gs[0, :])
    fig, ax1 = compose_plot(positions, position_args, fig, ax1)

    # Plot legends

    # TODO bar legends
    # TODO image legends: improve palettes vs legends
    geom_legends_funs = {
        "funkyrect": create_funkyrect_legend,
        "rect": create_rect_legend,
        "circle": create_circle_legend,
        "pie": create_pie_legend,
        "text": create_text_legend,
        "image": create_image_legend,
        "bar": create_bar_legend
    }

    enabled_legends = [legend for legend in legends if legend["enabled"]]
    for i, legend in enumerate(enabled_legends):
        if legend["geom"] in geom_legends_funs.keys():
            legend_ax = fig.add_subplot(gs[1, i])

            legend_fun = geom_legends_funs[legend["geom"]]
            legend["position_args"] = position_args
            legend_fun(**legend, ax = legend_ax)
    
    return fig


def get_plot_size(positions, position_args):
    minimum_x = positions["bounds"]["minimum_x"] - position_args.get("expand_xmin", 0)
    maximum_x = positions["bounds"]["maximum_x"] + position_args.get("expand_xmax", 0)
    minimum_y = positions["bounds"]["minimum_y"] - position_args.get("expand_ymin", 0)
    maximum_y = positions["bounds"]["maximum_y"] + position_args.get("expand_ymax", 0)

    return ((abs(minimum_x) + abs(maximum_x)) / 2, (abs(minimum_y) + abs(maximum_y)) / 2)