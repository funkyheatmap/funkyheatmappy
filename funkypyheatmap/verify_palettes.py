import pandas as pd
from pandas.api.types import is_numeric_dtype

default_palettes = {
    "numerical": ["Blues", "Reds", "YlOrBr", "Greens", "Greys"],
    "categorical": ["Set1", "Set2", "Set3", "Dark2"],
}


def verify_palettes(data, column_info, palettes=None):
    if palettes is None:
        palettes = {}

    # deframe palettes if it is a pandas dataframe
    if isinstance(palettes, pd.DataFrame):
        palettes = palettes.to_dict()

    # check palettes
    assert isinstance(palettes, dict), "palettes must be a dictionary"

    # check missing palettes
    col_info_palettes = column_info["palette"].dropna().unique()
    rotation_counter = {"numerical": 0, "categorical": 0}
    for palette_id in col_info_palettes:
        if palette_id not in palettes.keys():
            columns = column_info.loc[column_info["palette"] == palette_id, :].iloc[
                0, :
            ]

            if columns["geom"] == "pie":
                palette_type = "categorical"
            elif is_numeric_dtype(data[columns["id"]]):
                palette_type = "numerical"
            else:
                palette_type = "categorical"

            counter = rotation_counter[palette_type]
            palette_name = default_palettes[palette_type][counter]

            # increment counter
            counter += 1
            if counter > len(default_palettes[palette_type]) - 1:
                counter = 0
            rotation_counter[palette_type] = counter

            palettes[palette_id] = palette_name
        assert all(
            isinstance(palette, str) for palette in palettes.values()
        ), f"palettes must be strings"
        """
        pal_value = palettes[palette_id]
        if len(pal_value) == 1:
            if pal_value in default_palettes["numerical"]:
                pal_value = default_palettes["numerical"][pal_value]
            elif pal_value in default_palettes["categorical"]:
                pal_value = default_palettes["categorical"][pal_value]
        palettes[palette_id] = pal_value
        """
    return palettes

