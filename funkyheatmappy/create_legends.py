# from funkyheatmappy.score_to_funkyrectangle import score_to_funky_rectangle
from funkyheatmappy.compose_plot import compose_plot

import pandas as pd
import numpy as np

from matplotlib.colors import LinearSegmentedColormap

def score_to_funky_rectangle(row):#xmin, xmax, ymin, ymax, size_value, midpoint=0.5, name=None):
    xmin = row["xmin"]
    xmax = row["xmax"]
    ymin = row["ymin"]
    ymax = row["ymax"]
    size_value = row["size_value"]

    midpoint = 0.5

    if size_value is None:
        return None

    if size_value >= midpoint:
        trans = (size_value - midpoint) / (1 - midpoint) / 2 + 0.5
        corner_size = (0.9 - 0.8 * trans) * min(xmax - xmin, ymax - ymin)

        row["corner_size"] = corner_size

    else:
        trans = size_value / midpoint / 2
        start = 0
        end = 2 * np.pi
        x = xmin / 2 + xmax / 2
        y = ymin / 2 + ymax / 2
        r = (trans * 0.9 + 0.1) * min(xmax - xmin, ymax - ymin)

        row["trans"] = trans
        row["start"] = start
        row["end"] = end
        row["x"] = x
        row["y"] = y
        row["r"] = r
    
    return row

def create_title(title, start_x, start_y):
    title_data = pd.DataFrame(data = {
        "xmin": start_x,
        "xmax": start_x,
        "ymin": start_y - 1.5,
        "ymax": start_y - 0.5,
        "label_value": title,
        "ha": 0,
        "va": 1,
        "fontweight": "bold"
    }, index=["title"])

    return title_data

def create_label_data(labels, sizes, width, height, legend_space):
    legend_data = pd.DataFrame(data = {
        "label_value": labels,
        "width": width,
        "height": height,
        "ha": 0.5,
        "va": 0
    })

    legend_data["xmin"] = (legend_data["width"] + legend_space).cumsum() - legend_data["width"] - legend_space
    legend_data["xmin"] = legend_data["xmin"] - min(legend_data["xmin"])
    legend_data["xmax"] = legend_data["xmin"] + legend_data["width"]
    legend_data["ymin"] = -3.5
    legend_data["ymax"] = legend_data["ymin"] + legend_data["height"]

    return legend_data

def create_generic_geom_legend(title, geom, labels, size, color, position_args, label_hjust, ax = None):
    start_x = 0
    start_y = 0

    legend_size = 1
    legend_space = 0.2

    geom_data = pd.DataFrame(data = {
        "size_value": size,
        "color_value": color,
        "width": [x * legend_size for x in size],
        "height": [x * legend_size for x in size],
        "colour": color,
        "size": size,
        "label_hjust": label_hjust
    })

    geom_data["xmin"] = (geom_data["width"] + legend_space).cumsum() - geom_data["width"] - legend_space
    geom_data["xmin"] = start_x + geom_data["xmin"] - min(geom_data["xmin"])
    geom_data["xmax"] = geom_data["xmin"] + geom_data["width"]
    geom_data["ymin"] = start_y - 2.5
    geom_data["ymax"] = geom_data["ymin"] + geom_data["height"]
    geom_data["x"] = (geom_data["xmin"] + geom_data["xmax"]) / 2
    geom_data["y"] = (geom_data["ymin"] + geom_data["ymax"]) / 2
    geom_data["x0"] = geom_data["x"]
    geom_data["y0"] = geom_data["y"]

    if geom == "funkyrect":
        geom_data = geom_data.apply(score_to_funky_rectangle, axis=1)
    elif geom == "circle":
        geom_data["r"] = geom_data["size"] / 2

    title_data = create_title(title, start_x, start_y)
    label_data = create_label_data(labels, size, geom_data["width"], geom_data["height"], legend_space)
    text_data = pd.concat([title_data, label_data], axis=0)

    geom_positions = {
        "text_data": text_data,
        f"{geom}_data": geom_data
    }

    fig, ax = compose_plot(geom_positions, {}, ax = ax)

    return geom_positions

def create_funkyrect_legend(title, labels, size, color, position_args, label_hjust = .5, ax = None, **kwargs):
    return create_generic_geom_legend(title, "funkyrect", labels, size, color, position_args, label_hjust, ax = ax)

def create_rect_legend(title, labels, size, color, position_args, label_hjust = .5, ax = None, **kwargs):
    return create_generic_geom_legend(title, "rect", labels, size, color, position_args, label_hjust, ax = ax)

def create_bar_legend(title, labels, size, color, position_args, label_hjust = .5, ax = None, **kwargs):
    legend_width = 7
    legend_height = 1
    size = size[0]

    title_data = create_title(title, 0, 0)
    
    bar_data = pd.DataFrame(data = {
        "labels": [labels],
        "colourmap": LinearSegmentedColormap.from_list("custom", color, N = 200),
        "xmin": 0,
        "xmax": legend_width,
        "ymin": -2.5,
        "ymax": -1.5
    })

    width = [legend_width / len(labels)] * len(labels)
    heigth = [legend_height] * len(labels)

    label_data = create_label_data(labels, size, width, heigth, 0)


    geom_positions = {
        "bar_data": bar_data,
        "text_data": pd.concat([title_data, label_data], axis=0)
    }

    fig, ax = compose_plot(geom_positions, {}, ax = ax)

    return geom_positions

def create_circle_legend(title, labels, size, color, position_args, label_hjust = .5, ax = None, **kwargs):
    return create_generic_geom_legend(title, "circle", labels, size, color, position_args, label_hjust, ax = ax)

def create_text_legend(title, labels, size, color, values, position_args, label_width = 1, value_width = 2, ax = None, **kwargs):
    start_x = 0
    start_y = 0
    row_height = position_args["row_height"]

    geom_data = pd.DataFrame(data = {
        "label_value": labels,
        "colour": color,
        "va": 0.5,
        "ha": 1,
        "lab_y": [- row_height * i for i in range(len(labels))]
    })
    geom_data["x"] = start_x + 2 * .5 + label_width
    geom_data["y"] = start_y - 2 + geom_data["lab_y"]

    label_data = pd.DataFrame(data = {
        "label_value": values,
        "colour": color,
        "va": 0.5,
        "ha": 0,
        "lab_y": [- row_height * i for i in range(len(labels))]
    })
    label_data["x"] = start_x + 2 * .5 + label_width + value_width
    label_data["y"] = start_y - 2 + label_data["lab_y"]

    title_data = pd.DataFrame(data = {
        "x": start_x,
        "y": start_y - 1,
        "label_value": title,
        "ha": 0.5,
        "va": 1,
        "fontface": "bold",
        "colour": "black"
    }, index = [0])

    all_data = pd.concat([geom_data, label_data, title_data])

    all_data["xwidth"] = 2 * .5 + label_width + value_width
    all_data["yheight"] = row_height
    all_data["xmin"] = all_data["x"] - all_data["xwidth"] * all_data["ha"]
    all_data["xmax"] = all_data["x"] + all_data["xwidth"] * (1 - all_data["ha"])
    all_data["ymin"] = all_data["y"] - all_data["yheight"] * all_data["va"]
    all_data["ymax"] = all_data["y"] + all_data["yheight"] * (1 - all_data["va"])

    geom_positions = {
        "text_data": all_data
    }

    fig, ax2 = compose_plot(geom_positions, {}, ax = ax)
    ax.set_ylim([all_data["ymin"].min(), all_data["ymax"].max()])
    return fig

def create_pie_legend(title, labels, color, position_args, label_width = 2, ax = None, **kwargs):
    # we need pie title data
    # we need pie data
    # we need text data
    # we need segment data

    start_x = 0
    start_y = 0
    row_height = position_args["row_height"]

    legend_data = pd.DataFrame(data = {
        "name": labels,
        "fill": color
    })

    r = np.append(np.arange(90, -90, -(180 / len(labels))), [-90])
    angles = [i if i >= 0 else i + 360 for i in r]

    legend_data["start_angle"] = angles[1:len(labels) + 1]
    legend_data["end_angle"] = angles[0:len(labels)]
    legend_data["rad_start"] = np.linspace(0, np.pi, len(labels) + 1)[:-1]
    legend_data["rad_end"] = np.linspace(0, np.pi, len(labels) + 1)[1:]
    legend_data["rad"] = (legend_data["rad_start"] + legend_data["rad_end"]) / 2
    legend_data["color"] = "black"
    legend_data["labx"] = row_height * np.sin(legend_data["rad"][::-1])
    begin = row_height * np.cos(legend_data["rad"]).min() #- 0.4
    end = row_height * np.cos(legend_data["rad"]).max() #+ 0.4
    legend_data["laby"] = np.linspace(end, begin, len(labels))
    legend_data["ha"] = 0
    legend_data["va"] = 0.5
    legend_data["xpt"] = row_height * np.sin(legend_data["rad"])
    legend_data["ypt"] = row_height * np.cos(legend_data["rad"])

    # legen_pos = position_args["col_annot_offset"]
    title_data = pd.DataFrame(data = {
        "xmin": start_x,
        "xmax": start_x,
        "ymin": start_y - 1.5,
        "ymax": start_y - 0.5,
        "label_value": title,
        "ha": 0,
        "va": 1,
        "fontweight": "bold"
    }, index=["pie_title"])

    pie_data = pd.DataFrame(data = {
        "x0": start_x,
        "y0": start_y - 2.75,
        "height": row_height * 0.75,
        "start_angle": legend_data["start_angle"],
        "end_angle": legend_data["end_angle"],
        "colour": legend_data["fill"]
    })

    text_data = pd.DataFrame(data = {
        "xmin": start_x + 0.5 + legend_data["labx"],
        "xmax": start_x + 0.5 + legend_data["labx"],
        "ymin": start_y - 2.75 + legend_data["laby"] - 0.4,
        "ymax": start_y - 2.75 + legend_data["laby"] + 0.4,
        "label_value": legend_data["name"],
        "ha": legend_data["ha"],
        "va": legend_data["va"],
        "colour": legend_data["color"] #todo return to black
    })

    segment_data = pd.DataFrame(data = {
        "x": start_x + legend_data["xpt"] * 0.85,
        "xend": start_x + legend_data["xpt"] * 1.1,
        "y": start_y - 2.75 + legend_data["ypt"] * 0.85,
        "yend": start_y - 2.75 + legend_data["ypt"] * 1.1,
    })

    geom_positions = {
        "text_data": pd.concat([title_data, text_data]),
        "pie_data": pie_data,
        "segment_data": segment_data
    }

    fig, ax2 = compose_plot(geom_positions, {}, ax = ax)
    return fig

def create_image_legend(title, labels, values, position_args, label_width = 2, value_width = 1, ax = None, **kwargs):
    start_x = 0
    start_y = 0
    row_height = position_args["row_height"]

    image_data = pd.DataFrame(data = {
        "value": values,
        "va": 0.5,
        "ha": 1,
        "lab_y": [- row_height * i for i in range(len(labels))]
    })
    image_data["x"] = start_x + 2 * .5 + value_width
    image_data["y"] = start_y - 2 + image_data["lab_y"]
    size = min(2 * .5 + value_width, row_height)
    image_data["xwidth"] = size
    image_data["yheight"] = size

    image_data["xmin"] = image_data["x"] - image_data["xwidth"] * image_data["ha"]
    image_data["xmax"] = image_data["x"] + image_data["xwidth"] * (1 - image_data["ha"])
    image_data["ymin"] = image_data["y"] - image_data["yheight"] * image_data["va"]
    image_data["ymax"] = image_data["y"] + image_data["yheight"] * (1 - image_data["va"])

    label_data = pd.DataFrame(data = {
        "label_value": labels,
        "va": 0.5,
        "ha": 0,
        "lab_y": [- row_height * i for i in range(len(labels))]
    })
    label_data["x"] = start_x + 2 * .5 + value_width + label_width
    label_data["y"] = start_y - 2 + label_data["lab_y"]

    title_data = pd.DataFrame(data = {
        "x": start_x,
        "y": start_y - 1,
        "label_value": title,
        "ha": 0.5,
        "va": 1,
        "fontface": "bold"
    }, index = [0])

    text_data = pd.concat([label_data, title_data])

    text_data["xwidth"] = 2 * .5 + value_width + label_width
    text_data["yheight"] = row_height
    text_data["xmin"] = text_data["x"] - text_data["xwidth"] * text_data["ha"]
    text_data["xmax"] = text_data["x"] + text_data["xwidth"] * (1 - text_data["ha"])
    text_data["ymin"] = text_data["y"] - text_data["yheight"] * text_data["va"]
    text_data["ymax"] = text_data["y"] + text_data["yheight"] * (1 - text_data["va"])

    geom_positions = {
        "image_data": image_data,
        "text_data": text_data
    }

    fig, ax2 = compose_plot(geom_positions, {}, ax = ax)
    ax.set_ylim([text_data["ymin"].min(), text_data["ymax"].max()])
    return fig
