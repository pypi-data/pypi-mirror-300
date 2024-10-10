import pandas as pd

def rename_select_columns(df: pd.DataFrame, column_rename_dict: dict) -> pd.DataFrame:
    """

    changes the name of dataframe columns and filters to columns in the dictionary.
    assigning new value to None includes the column but does not rename it

    Args:
        df: dataframe to modify
        column_rename_dict: dictionary of column values {old_name:new_name}

    Returns: dataframe only containing specified columns

    """

    column_rename_dict = {k: (v if v is not None else k) for (k, v) in column_rename_dict.items()}

    df1 = df.copy()
    target_columns = list(column_rename_dict.keys())
    for col in target_columns:
        if col not in df1.columns:
            raise KeyError(f"Column: ({col}) not found in dataframe.")
    df1 = df1[target_columns]
    df1 = df1.rename(columns=column_rename_dict)

    return df1