import matplotlib
import pandas as pd
from pandas.api.types import is_numeric_dtype
import matplotlib.cm as cm


color_dict = dict(
    zip(
        ["Blues", "Reds", "YlOrBr", "Greens", "Greys", "Set3", "Set1", "Set2", "Dark2"],
        [
            cm.Blues_r,
            cm.Reds_r,
            cm.YlOrBr_r,
            cm.Greens_r,
            cm.Greys_r,
            cm.Set3,
            cm.Set1,
            cm.Set2,
            cm.Dark2,
        ],
    )
)

for cmap in color_dict.keys():
    if cmap in ["Blues", "Reds", "YlOrBr", "Greens", "Greys"]:
        vmax = 101
    elif cmap == "Set3":
        vmax = 12
    elif cmap == "Set1":
        vmax = 9
    else:
        vmax = 8
    norm = matplotlib.colors.Normalize(vmin=0, vmax=vmax, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=color_dict[cmap])
    colors = [mapper.to_rgba(i) for i in range(0, vmax)]
    color_dict[cmap] = colors

default_palettes = {
    "numerical": {
        "Blues": color_dict["Blues"],
        "Reds": color_dict["Reds"],
        "YlOrBr": color_dict["YlOrBr"],
        "Greens": color_dict["Greens"],
        "Greys": color_dict["Greys"],
    },
    "categorical": {
        "Set1": color_dict["Set1"],
        "Set2": color_dict["Set2"],
        "Set3": color_dict["Set3"],
        "Dark2": color_dict["Dark2"],
    },
}


def verify_palettes(data, column_info, palettes=None):
    if palettes is None:
        palettes = {}

    # deframe palettes if it is a pandas dataframe
    if isinstance(palettes, pd.DataFrame):
        palettes = {row["palettes"]: row["colours"] for _, row in palettes.iterrows()}

    # check palettes
    assert isinstance(palettes, dict), "palettes must be a dictionary"

    # check missing palettes
    col_info_palettes = column_info["palette"].dropna().unique()
    rotation_counter = {"numerical": 0, "categorical": 0}
    for palette_id in col_info_palettes:
        if palette_id not in palettes.keys():
            columns_tmp = column_info.loc[column_info["palette"] == palette_id, :]
            columns = columns_tmp.iloc[0, :]

            if columns["geom"] == "pie":
                palette_type = "categorical"
            elif is_numeric_dtype(data[columns_tmp.index[0]]):
                palette_type = "numerical"
            else:
                palette_type = "categorical"

            counter = rotation_counter[palette_type]
            palette_name = list(default_palettes[palette_type].keys())[counter]

            # increment counter
            counter += 1
            if counter > len(default_palettes[palette_type]) - 1:
                counter = 0
            rotation_counter[palette_type] = counter

            palettes[palette_id] = palette_name
        assert isinstance(palettes[palette_id], str), f"palettes must be strings"

        pal_value = palettes[palette_id]

        if isinstance(pal_value, str):
            if pal_value in list(default_palettes["numerical"].keys()):
                pal_value = default_palettes["numerical"][pal_value]
            elif pal_value in list(default_palettes["categorical"].keys()):
                pal_value = default_palettes["categorical"][pal_value]
        palettes[palette_id] = pal_value

    return palettes

