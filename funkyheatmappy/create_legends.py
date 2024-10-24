# from funkyheatmappy.score_to_funkyrectangle import score_to_funky_rectangle
from funkyheatmappy.compose_plot import compose_plot

import pandas as pd
import numpy as np

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


def create_generic_geom_legend(title, geom, labels, size, color, position_args, label_hjust, ax = None):
    start_x = 0
    start_y = 0

    legend_size = 1
    legend_space = 0.2

    legend_data = pd.DataFrame(data = {
        "size_value": size,
        "color_value": color,
        "xmin": [x * -1 * legend_size / 2 for x in size],
        "xmax": [x * legend_size / 2 for x in size],
        "ymin": [x * -1 * legend_size / 2 for x in size],
        "ymax": [x * legend_size / 2 for x in size],
        "label": labels,
        "colour": color,
        "size": size,
        "label_hjust": label_hjust
    })

    if geom == "funkyrect":
        legend_data = legend_data.apply(score_to_funky_rectangle, axis=1)
        # legend_data = legend_data.apply(score_to_funky_rectangle, axis=1)
    elif geom == "circle":
        legend_data["r"] = legend_data["size"] / 2

    geom_data = legend_data.copy()

    geom_data["width"] = geom_data["xmax"] - geom_data["xmin"]
    geom_data["w"] = geom_data["width"]
    geom_data["height"] = geom_data["ymax"] - geom_data["ymin"]
    geom_data["h"] = geom_data["height"]
    geom_data["xmin"] = (geom_data["width"] + legend_space).cumsum() - geom_data["width"] - legend_space
    geom_data["xmin"] = start_x + geom_data["xmin"] - min(geom_data["xmin"])
    geom_data["xmax"] = geom_data["xmin"] + geom_data["width"]
    geom_data["ymin"] = start_y - 2.5
    geom_data["ymax"] = geom_data["ymin"] + geom_data["height"]
    geom_data["x"] = (geom_data["xmin"] + geom_data["xmax"]) / 2
    geom_data["y"] = (geom_data["ymin"] + geom_data["ymax"]) / 2
    geom_data["x0"] = geom_data["x"]
    geom_data["y0"] = geom_data["y"]

    maximum_x = max(geom_data["xmax"])

    title_data = pd.DataFrame(data = {
        "xmin": start_x,
        "xmax": maximum_x,
        "ymin": start_y - 1.5,
        "ymax": start_y - 0.5,
        "label_value": title,
        "hjust": 0,
        "vjust": 1,
        "fontface": "bold"
    }, index = [0])

    necessary_geom_data = geom_data[["xmin", "xmax", "ymin", "ymax"]]
    necessary_geom_data["ymin"] = necessary_geom_data["ymin"] - 1
    necessary_geom_data["hjust"] = geom_data["label_hjust"]
    necessary_geom_data["vjust"] = 0
    necessary_geom_data["ha"] = necessary_geom_data["hjust"]
    necessary_geom_data["va"] = necessary_geom_data["vjust"]
    necessary_geom_data["label_value"] = geom_data["label"]
    necessary_geom_data["w"] = geom_data["width"]
    necessary_geom_data["h"] = geom_data["height"]

    text_data = pd.concat([title_data, necessary_geom_data], axis=0)
    text_data["x"] = (1 - text_data["hjust"]) * text_data["xmin"] + text_data["hjust"] * text_data["xmax"]
    text_data["y"] = (1 - text_data["vjust"]) * text_data["ymin"] + text_data["vjust"] * text_data["ymax"]

    geom_positions = {
        "text_data": text_data,
        f"{geom}_data": geom_data
    }

    # return compose_plot(geom_positions, [])
    fig, ax2 = compose_plot(geom_positions, {}, ax = ax)
    # fig, ax2 = compose_plot(geom_positions, {})
    # fig.savefig("legend.png")
    return geom_positions


def create_funkyrect_legend(title, labels, size, color, position_args, label_hjust = .5, ax = None, **kwargs):
    return create_generic_geom_legend(title, "funkyrect", labels, size, color, position_args, label_hjust, ax = ax)

def create_rect_legend(title, labels, size, color, position_args, label_hjust = .5, ax = None, **kwargs):
    return create_generic_geom_legend(title, "rect", labels, size, color, position_args, label_hjust, ax = ax)

def create_circle_legend(title, labels, size, color, position_args, label_hjust = .5, ax = None, **kwargs):
    return create_generic_geom_legend(title, "circle", labels, size, color, position_args, label_hjust, ax = ax)

def create_text_legend(title, labels, size, color, values, position_args, label_width = 1, value_width = 2, ax = None, **kwargs):
    start_x = 0
    start_y = 0
    row_height = position_args["row_height"]

    legend_data = pd.DataFrame(data = {
        "name": labels,
        "value": values,
        "colour": color,
        "size": size,
        "vjust": 0.5,
        "hjust": 0,
        "lab_y": [- row_height * i for i in range(len(labels))]
    })

    text_data = pd.DataFrame(data = {
        "x": start_x,
        "y": start_y - 1,
        "label_value": title,
        "hjust": 0,
        "vjust": 1,
        "fontface": "bold",
        "colour": "black"
    })

    text_data["x"] = start_x + 0.5
    text_data["y"] = start_y - 2 + legend_data["lab_y"]
    text_data["label_value"] = legend_data["name"]
    text_data["vjust"] = legend_data["vjust"]
    text_data["hjust"] = legend_data["hjust"]
    text_data["colour"] = legend_data["colour"]

    text_data["x"] = start_x + 2 * .5 + label_width
    text_data["y"] = start_y - 2 + legend_data["lab_y"]
    text_data["label_value"] = legend_data["value"]
    text_data["vjust"] = legend_data["vjust"]
    text_data["hjust"] = legend_data["hjust"]
    text_data["colour"] = legend_data["colour"]

    text_data["x_width"] = 2 * .5 + label_width + value_width
    text_data["y_height"] = row_height
    text_data["xmin"] = text_data["x"] - text_data["x_width"] * text_data["hjust"]
    text_data["xmax"] = text_data["x"] + text_data["x_width"] * (1 - text_data["hjust"])
    text_data["ymin"] = text_data["y"] - text_data["y_height"] * text_data["vjust"]
    text_data["ymax"] = text_data["y"] + text_data["y_height"] * (1 - text_data["vjust"])

    geom_positions = {
        "text_data": text_data
    }

    fig, ax2 = compose_plot(geom_positions, {})
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
    legend_data["labx"] = row_height * np.sin(legend_data["rad"])
    begin = row_height * np.cos(legend_data["rad"]).min() #- 0.4
    end = row_height * np.cos(legend_data["rad"]).max() #+ 0.4
    legend_data["laby"] = np.linspace(begin, end, len(labels))
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
        "colour": legend_data["color"]
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


