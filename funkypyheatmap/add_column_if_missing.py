import numpy as np


def add_column_if_missing(df, **kwargs):
    column_values = kwargs
    for col_keys, col_values in column_values.items():
        default_val = np.repeat(col_values, df.shape[0])
        if col_keys in df.columns:
            df[col_keys] = df[col_keys].fillna(default_val)
        else:
            df[col_keys] = default_val
    return df