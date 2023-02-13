import pandas as pd


def verify_data(data):
    """Check if data is panda dataframe and if matrix it makes a pandas"""
    assert isinstance(data, pd.DataFrame), "data must be a pandas dataframe"
    assert (
        data.shape[0] >= 1 and data.shape[1] >= 1
    ), "data must be a dataframe with at least 1 row and 1 column"
    if "id" in data.columns:
        data = data.set_index("id")
    return data