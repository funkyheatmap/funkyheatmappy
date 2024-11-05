import pandas as pd


def verify_data(data):
    """Verify that the data is a pandas dataframe with at least 1 row and 1 column. If an id column is present, set it as the index."""
    
    assert isinstance(data, pd.DataFrame), "data must be a pandas dataframe"
    assert (
        data.shape[0] >= 1 and data.shape[1] >= 1
    ), "data must be a dataframe with at least 1 row and 1 column"
    if "id" in data.columns:
        data = data.set_index(data["id"])
    else:
        data.index = data.index.astype(str)
    return data
