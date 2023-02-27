"""
Tests for `funkypyheatmap` module.
"""
import pytest
from funkypyheatmap import funkypyheatmap
import pandas as pd


@pytest.fixture(scope="session")
def mtcars():
    mtcars = pd.read_csv("./test/data/mtcars.csv")
    mtcars = mtcars.rename(columns={"Unnamed: 0": "id"})
    return mtcars


class TestFunkypyheatmap(object):
    def test_mtcars(self, mtcars):
        mtcars = mtcars.rename(columns={"Unnamed: 0": "id"})
        funkypyheatmap.funkyheatmap(mtcars)

    def test_mtcars_extended(self, mtcars):
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
                    {"hjust": 0, "width": 6},
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
            }
        )
        column_info.index = column_info["id"]
        column_groups = pd.DataFrame(
            {
                "Category": ["Overall", "Group1", "Group2"],
                "group": ["overall", "group1", "group2"],
            }
        )
        row_info = pd.DataFrame(
            {"id": mtcars["id"], "group": "test"}, index=mtcars["id"]
        )
        row_groups = pd.DataFrame({"Group": ["Test"], "group": ["test"]})
        funkypyheatmap.funkyheatmap(
            data=mtcars,
            column_info=column_info,
            column_groups=column_groups,
            row_info=row_info,
            row_groups=row_groups,
            expand={"xmax": 4},
        )
        print("hello world")
