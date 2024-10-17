from .compose_plot import compose_plot

import pandas as pd

def score_to_funky_rectangle(row):
    xmin = row["xmin"]
    xmax = row["xmax"]
    ymin = row["ymin"]
    ymax = row["ymax"]
    size_value = row["size_value"]

    midpoint = 0.8

    if size_value == None:
        return None
    
    if size_value >= midpoint:
        # transform value to 0.5 .. 1.0 range
        trans = (size_value - midpoint) / (1 - midpoint) / 2 + 0.5
        row["corner_size"] = (0.9 - 0.8 * trans) * min(xmax - xmin, ymax - ymin)
    
    else:
        x = xmin / 2 + xmax / 2
        y = ymin / 2 + ymax / 2
        row["corner_size"] = 0.5

        trans = size_value / midpoint

        width = (trans * 0.9 + 0.1) * min(xmax - xmin, ymax - ymin)
        row["xmin"] = x - width / 2
        row["xmax"] = x + width / 2
        row["ymin"] = y - width / 2
        row["ymax"] = y + width / 2
    
    return row


def create_generic_geom_legend(title, geom, labels, size, color, position_args, label_hjust):
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
        "color": color,
        "size": size,
        "label_hjust": label_hjust
    })

    if geom == "funkyrect":
        legend_data = legend_data.apply(score_to_funky_rectangle, axis=1)
    elif geom == "circle":
        legend_data["r"] = legend_data["size"] / 2

    geom_data = legend_data.copy()

    geom_data["width"] = geom_data["xmax"] - geom_data["xmin"]
    geom_data["height"] = geom_data["ymax"] - geom_data["ymin"]
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
    necessary_geom_data["label_value"] = geom_data["label"]

    text_data = pd.concat([title_data, necessary_geom_data], axis=0)
    text_data["x"] = (1 - text_data["hjust"]) * text_data["xmin"] + text_data["hjust"] * text_data["xmax"]
    text_data["y"] = (1 - text_data["vjust"]) * text_data["ymin"] + text_data["vjust"] * text_data["ymax"]

    geom_positions = {
        "text_data": text_data,
        f"{geom}_data": geom_data
    }

    # return compose_plot(geom_positions, [])
    fig, ax2 = compose_plot(geom_positions, {})
    fig.savefig("legend.png")
    return fig


def create_funkyrect_legend(title, labels, size, color, position_args, label_hjust = .5, **kwargs):
    return create_generic_geom_legend(title, "funkyrect", labels, size, color, position_args, label_hjust)

def create_rect_legend(title, labels, size, color, position_args, label_hjust = .5, **kwargs):
    return create_generic_geom_legend(title, "rect", labels, size, color, position_args, label_hjust)

def create_circle_legend(title, labels, size, color, position_args, label_hjust = .5, **kwargs):
    return create_generic_geom_legend(title, "circle", labels, size, color, position_args, label_hjust)

def create_text_legend(title, labels, size, color, values, position_args, label_width = 1, value_width = 2, **kwargs):
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




