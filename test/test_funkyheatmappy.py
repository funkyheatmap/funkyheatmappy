"""
Tests for `funkyheatmappy` module.
"""
import matplotlib
import pytest
from funkyheatmappy import funkyheatmappy
from funkyheatmappy.position_arguments import position_arguments
import pandas as pd
import numpy as np
import matplotlib.cm as cm


@pytest.fixture(scope="session")
def mtcars():
    mtcars = pd.read_csv("./test/data/mtcars.csv")
    mtcars = mtcars.rename(columns={"Unnamed: 0": "id"})
    column_info = pd.DataFrame(
        {
            "id": mtcars.columns,
            "group": [
                pd.NA,
                "overall",
                "overall",
                "group1",
                "group1",
                "group1",
                "group1",
                "group2",
                "group2",
                "group2",
                "group2",
                "group2",
            ],
            "name": [
                "",
                "Miles / gallon",
                "Number of cylinders",
                "Displacement (cu.in.)",
                "Gross horsepower",
                "Rear axle ratio",
                "Weight (1000 lbs)",
                "1/4 mile time",
                "Engine",
                "Transmission",
                "# Forward gears",
                "# Carburetors",
            ],
            "geom": [
                "text",
                "bar",
                "bar",
                "funkyrect",
                "funkyrect",
                "funkyrect",
                "funkyrect",
                "circle",
                "circle",
                "circle",
                "circle",
                "circle",
            ],
            "options": [
                {"ha": 0, "width": 6},
                {"width": 4, "legend": False},
                {"width": 4, "legend": False},
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
            ],
            "palette": [
                np.nan,
                "palette1",
                "palette2",
                "palette1",
                "palette1",
                "palette1",
                "palette1",
                "palette2",
                "palette2",
                "palette2",
                "palette2",
                "palette2",
            ],
        }
    )
    column_info.index = column_info["id"]
    column_groups = pd.DataFrame(
        {
            "Category": ["Overall", "Group1", "Group2"],
            "group": ["overall", "group1", "group2"],
            "palette": ["overall", "palette1", "palette2"],
        }
    )
    row_info = pd.DataFrame({"id": mtcars["id"], "group": "test"}, index=mtcars["id"])
    row_groups = pd.DataFrame({"Group": ["Test"], "group": ["test"]})
    norm = matplotlib.colors.Normalize(vmin=0, vmax=101, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap="Greys")
    colors = [mapper.to_rgba(i) for i in range(0, 101)]
    palettes = pd.DataFrame(
        {
            "palettes": ["overall", "palette1", "palette2"],
            "colours": [colors, "Blues", "Reds"],
        }
    )
    return {
        "data": mtcars,
        "column_info": column_info,
        "column_groups": column_groups,
        "row_info": row_info,
        "row_groups": row_groups,
        "palettes": palettes,
    }


@pytest.fixture(scope="session")
def dynbenchmark_data():
    pies = pd.read_csv("./test/data/dynbenchmark_pie.csv", header=0, index_col=0)
    data = pd.read_csv("./test/data/dynbenchmark_data.csv")
    data["benchmark_overall_error_reasons"] = pies.to_dict("index").values()
    column_groups = pd.read_csv("./test/data/dynbenchmark_column_groups.csv")
    column_info = pd.read_csv(
        "./test/data/dynbenchmark_column_info.csv",
        index_col="id",
        keep_default_na=False,
        na_values=["NaN"],
    )
    row_groups = pd.read_csv("./test/data/dynbenchmark_row_groups.csv")
    row_info = pd.read_csv("./test/data/dynbenchmark_row_info.csv", index_col="id")
    palettes = pd.read_csv("./test/data/dynbenchmark_palettes.csv")
    palettes["colours"] = palettes.colours.apply(lambda x: x.split(", "))
    names_error_r = [
        "Memory limit exceeded",
        "Time limit exceeded",
        "Execution error",
        "Method error",
    ]
    options = pd.read_csv("./test/data/dynbenchmark_options.csv")
    options = [
        {k: v for k, v in m.items() if pd.notnull(v)}
        for m in options.to_dict(orient="records")
    ]

    column_info["options"] = options
    column_info.loc["method_priors_required_str", "options"]["legend"] = {
        "legend": {
            "": "None",
            "✕": "Weak: Start or end cells",
            "✖": "Strong: Cell grouping or time course",
        }
    }
    palettes["colours"][5] = dict(zip(names_error_r, palettes["colours"][5]))
    return {
        "data": data,
        "column_groups": column_groups,
        "column_info": column_info,
        "row_groups": row_groups,
        "row_info": row_info,
        "palettes": palettes,
    }


class Testfunkyheatmappy(object):
    def test_mtcars(self, mtcars):
        funkyheatmappy.funky_heatmap(mtcars["data"])


    def test_mtcars_extended(self, mtcars):
        mtcars["data"] = (
            mtcars["data"].sort_values(by="mpg", ascending=False).reset_index(drop=True)
        )
        funkyheatmappy.funky_heatmap(
            data=mtcars["data"],
            column_info=mtcars["column_info"],
            column_groups=mtcars["column_groups"],
            row_info=mtcars["row_info"],
            row_groups=mtcars["row_groups"],
            palettes=mtcars["palettes"],
            position_args=position_arguments(expand_xmax=4),
        )

    def test_mtcars_images(self, mtcars):
        mtcars["data"]["type"] = np.concatenate(
            (np.repeat("ice", 10), np.repeat("electric", 22))
        )
        mtcars["column_info"] = pd.concat(
            [
                mtcars["column_info"],
                pd.DataFrame(
                    {
                        "id": ["type"],
                        "group": ["group2"],
                        "name": ["Type of engine"],
                        "geom": ["image"],
                        "options": [{"path": "./test/data/", "filetype": "png"}],
                        "palette": [np.nan],
                    },
                    index=["type"],
                ),
            ]
        )
        funkyheatmappy.funky_heatmap(
            data=mtcars["data"],
            column_info=mtcars["column_info"],
            column_groups=mtcars["column_groups"],
            row_info=mtcars["row_info"],
            row_groups=mtcars["row_groups"],
            palettes=mtcars["palettes"],
            position_args=position_arguments(expand_xmax=4),
        )


    def test_dynbenchmark(self, dynbenchmark_data):
        funkyheatmappy.funky_heatmap(
            data=dynbenchmark_data["data"],
            column_info=dynbenchmark_data["column_info"],
            column_groups=dynbenchmark_data["column_groups"],
            row_info=dynbenchmark_data["row_info"],
            row_groups=dynbenchmark_data["row_groups"],
            palettes=dynbenchmark_data["palettes"],
            position_args=position_arguments(col_annot_offset=4.2),
        )


    def test_position_arguments(self, dynbenchmark_data):
        pos_arg = position_arguments(
            row_height=4,
            row_space=4,
            row_bigspace=4,
            col_width=4,
            col_space=4,
            col_bigspace=4,
            col_annot_angle=4,
            col_annot_offset=3.2,
            expand_xmin=4,
            expand_xmax=4,
            expand_ymin=4,
            expand_ymax=4,
        )

        funkyheatmappy.funky_heatmap(
            data=dynbenchmark_data["data"],
            column_info=dynbenchmark_data["column_info"],
            column_groups=dynbenchmark_data["column_groups"],
            row_info=dynbenchmark_data["row_info"],
            row_groups=dynbenchmark_data["row_groups"],
            palettes=dynbenchmark_data["palettes"],
            position_args=pos_arg,
        )
