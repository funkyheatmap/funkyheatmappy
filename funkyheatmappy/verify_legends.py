import numpy as np

def verify_legends(legends, palettes, column_info, data):

    if legends is None:
        print("No legends were provided, trying to automatically infer legends.")
        legends = []

    # deframe --> not necessary?

    assert isinstance(legends, list), "legends must be a list"

    palettes_in_col_info = column_info["palette"].unique()  
    palettes_in_palette_names = palettes.keys()
    used_palettes = set(palettes_in_col_info).intersection(palettes_in_palette_names)
    palettes_in_legends = set([legend["palette"] for legend in legends if "palette" in legend])

    missing_palettes = used_palettes - palettes_in_legends

    if len(missing_palettes) > 0:
        print("Some palettes were not used in the column info, adding legends for them:" + ", ".join(missing_palettes))

        for i in range(len(missing_palettes)):
            palette = missing_palettes.pop()
            legend = {
                "title": palette,
                "palette": palette,
                "enabled": True,
            }
            legends.append(legend)

    legends_verified = []

    for legend in legends:
        verified_legend = verify_single_legend(legend, palettes, column_info)
        legends_verified.append(verified_legend)

    return legends_verified

        
def verify_single_legend(legend, palettes, column_info):
    assert isinstance(legend, dict), "each legend must be a dictionary"

    if "palette" in legend:
        assert legend["palette"] in palettes, "palette must be a key in palettes"
        assert isinstance(legend["palette"], str), "palette must be a string"

    # check enabled
    if "enabled" not in legend:
        legend["enabled"] = True
    assert isinstance(legend["enabled"], bool), "enabled must be a boolean"
    if not legend["enabled"]:
        return legend
    
    # check title
    if "title" not in legend and "palette" in legend:
        print(f"Legend {legend} did not contain a title, using the name of the palette as title.")
        legend["title"] = legend["palette"]
    assert "title" in legend, "legend must have a title"
    assert isinstance(legend["title"], str), "title must be a string"

    # check geom
    if "geom" not in legend and "palette" in legend:
        print(f"Legend {legend} did not contain a geom, inferring from the column_info.")
        legend["geom"] = column_info.loc[column_info["palette"] == legend["palette"], "geom"].iloc[0]
    assert "geom" in legend, "legend must have a geom"
    assert legend["geom"] in ["circle", "rect", "funkyrect", "text", "pie", "continuous", "discrete", "bar"], "geom must be one of 'circle', 'rect', 'funkyrect', 'text', 'pie', 'continuous', 'discrete', 'bar'"
    
    if legend["geom"] == "bar":
        print(f"Legend {legend} has a geom of 'bar', which is not yet supported. Skipping this legend.")
        legend["enabled"] = False
        return legend

    # check labels
    if "labels" not in legend:
        print(f"Legend {legend} did not contain labels, inferring from the geom.")
        
        if legend["geom"] == "pie" and "palette" in legend:
            legend["labels"] = palettes[legend["palette"]].keys()
        elif legend["geom"] in ["circle", "rect", "funkyrect"]:
            legend["labels"] = ["0", "", "0.2", "", "0.4", "", "0.6", "", "0.8", "", "1"]
        elif legend["geom"] == "text":
            print(f"Legend {legend} has geom 'text' but no specified labels, so disabling this legend for now.")
            legend["enabled"] = False
            return legend
        # assert that it is a list of strings
    assert isinstance(legend["labels"], list), "labels must be a list"
    assert all(isinstance(s, str) for s in legend["labels"]), "labels must be strings"

    # check size
    if legend["geom"] in ["circle", "rect", "funkyrect", "text"]:
        if "size" not in legend:
            if legend["geom"] == "text":
                legend["size"] = 3.88
            else:
                print(f"Legend {legend} did not contain size, inferring from the labels.")
                legend["size"] = np.linspace(0, 1, len(legend["labels"]))

        assert isinstance(legend["size"], list), "size must be a list"
        assert all(isinstance(s, (int, float)) for s in legend["size"]), "size must be a list of numbers"
        # assert that it is the same length as labels or 1
        assert len(legend["size"]) == 1 or len(legend["size"]) == len(legend["labels"]), "size must be the same length as labels or 1"

    if len(legend["size"]) == 1:
        legend["size"] = [legend["size"][0]] * len(legend["labels"])

    # check color
    if "colour" in legend:
        legend["color"] = legend["colour"]
        del legend["colour"]
    
    if "color" not in legend:
        if "palette" in legend:
            print(f"Legend {legend} did not contain color, inferring from the palette.")
            colors = palettes[legend["palette"]].values()
            legend["color"] = colors[round(np.linspace(0, len(colors), len(legend["labels"])))]
        elif legend["geom"] == "text":
            legend["color"] = "black"
    # assert list of strings
    # assert length is the same as labels or 1
    assert isinstance(legend["color"], list), "color must be a list"
    assert all(isinstance(s, str) for s in legend["color"]), "color must be a list of strings"
    assert len(legend["color"]) == 1 or len(legend["color"]) == len(legend["labels"]), "color must be the same length as labels or 1"

    # check hjust
    if "label_hjust" not in legend:
        if legend["geom"] in ["circle", "rect", "funkyrect"]:
            legend["label_hjust"] = 0.5
        else:
            legend["label_hjust"] = None
    
    if "label_hjust" in legend:
        # assert list of int or float
        # assert lenght is the same as labels or 1
        assert isinstance(legend["label_hjust"], (int, float, list)), "label_hjust must be a number"
        assert len(legend["label_hjust"]) == 1 or len(legend["label_hjust"]) == len(legend["labels"]), "label_hjust must be the same length as labels or 1"

        if len(legend["label_hjust"]) == 1:
            legend["label_hjust"] = [legend["label_hjust"][0]] * len(legend["labels"])

    # check label_width
    if "label_width" not in legend:
        if legend["geom"] == "text":
            legend["label_width"] = 1
        elif legend["geom"] == "pie":
            legend["label_width"] = 2
        else:
            legend["label_width"] = None
        
    if "label_width" in legend:
        assert isinstance(legend["label_width"], (int, float)), "label_width must be a number"
        assert len(legend["label_width"]) == 1, "label_width must be a single number"

    # check value_width
    if "value_width" not in legend:
        if legend["geom"] == "text":
            legend["value_width"] = 2
        else:
            legend["value_width"] = None
    
    if "value_width" in legend:
        assert isinstance(legend["value_width"], (int, float)), "value_width must be a number"
        assert len(legend["value_width"]) == 1, "value_width must be a single number"
    
    return legend
