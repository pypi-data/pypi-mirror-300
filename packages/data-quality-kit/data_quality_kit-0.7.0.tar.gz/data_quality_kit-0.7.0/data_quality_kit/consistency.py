from pandas import DataFrame


def assert_that_columns_values_match(df1: DataFrame, primary_key_column: str, df2: DataFrame, foreign_key_column: str) -> bool:
    """
    Check if all values in column2 of df2 are present in column1 of df1.

    Parameters:
    df1 : The first DataFrame to check.
    column1 : The column in the first DataFrame to check for matches.
    df2 : The second DataFrame to check.
    column2 : The column in the second DataFrame to check for matches.

    Returns:
    bool: True if all values in column2 of df2 are present in column1 of df1, 
    False otherwise.

    Raises:
    ValueError: If either column does not exist in its respective DataFrame.
    """
    if primary_key_column not in df1.columns:
        raise ValueError(
            f'Error: The column "{primary_key_column}" does not exist in the first DataFrame.')
    if foreign_key_column not in df2.columns:
        raise ValueError(
            f'Error: The column "{foreign_key_column}" does not exist in the second DataFrame.')
    return df2[foreign_key_column].isin(df1[primary_key_column]).all()


def assert_that_there_are_not_duplicates(df: DataFrame, pk_column: str) -> bool:
    """
    Checks for duplicate values in the specified primary key column of a DataFrame.

    Parameters:
    df : The DataFrame to check.
    pk_column : The name of the primary key column to check for duplicates.

    Returns:
    bool: True if there are duplicate values in the primary key column, False if there are no duplicates.

    Raises:
    ValueError: If the pk_column is not a column in the DataFrame.
    """
    if pk_column not in df.columns:
        raise ValueError(f'Column "{pk_column}" not in DataFrame.')

    return df[pk_column].duplicated().any()
