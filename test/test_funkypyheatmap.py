"""
Tests for `funkypyheatmap` module.
"""
import pytest
from funkypyheatmap import funkypyheatmap
import pandas as pd


@pytest.fixture(scope="session")
def mtcars():
    return pd.read_csv("./test/data/mtcars.csv")


class TestFunkypyheatmap(object):
    def test_mtcars(self, mtcars):
        mtcars = mtcars.rename(columns={"Unnamed: 0": "id"})
        funkypyheatmap.funkyheatmap(mtcars)
