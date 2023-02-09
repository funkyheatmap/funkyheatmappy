"""
Tests for `funkypyheatmap` module.
"""
import pytest
from funkypyheatmap import funkypyheatmap
import pandas as pd

@pytest.fixture(scope="session")
def mtcars():
    return pd.read_csv("./tests/data/mtcars.csv")

class TestFunkypyheatmap(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self, mtcars):
        funkypyheatmap.funkyheatmap(mtcars)
        

    @classmethod
    def teardown_class(cls):
        pass
