import pandas as pd

def verify_column_info(data, column_info = None):
    if column_info is None:
        column_info = pd.DataFrame(columns = data.columns)
    
    assert isinstance(column_info, pd.DataFrame), "column_info must be a pandas dataframe"
    assert "id" in column_info.columns, "column_info must have a column named 'id'"
    assert all(column_info["id"].isin(data.columns)), "column_info must have the same ids as data"
    
    