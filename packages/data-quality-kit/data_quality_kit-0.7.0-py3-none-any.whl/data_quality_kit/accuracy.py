import pandas as pd


def assert_that_type_value(df: pd.DataFrame, column_name: str, data_type: type) -> bool:
    """
    Check if all non-null entries in a specified column of a DataFrame are of the specified data type.

    Args:
        df : The DataFrame to check.
        column_name : The name of the column to check.
        data_type : The expected data type of the column entries.

    Returns:
        bool: True if all non-null entries in the specified column are of the specified data type, False otherwise.

    Raises:
        ValueError: If the column does not exist in the DataFrame or if at least one entry is not of the specified data type.
    """
    if column_name not in df.columns:
        raise ValueError(f'Column "{column_name}" not in DataFrame.')

    filtered_values = df[df[column_name].notnull()]
    return filtered_values[column_name].apply(lambda x: isinstance(x, data_type)).all()


def assert_that_values_in_catalog(dataframe: pd.DataFrame, column: str, catalog: list):
    """
    Checks whether all values in the specified column of a DataFrame are present
    in a catalog (list of values).

    Parameters:
    ----------
    dataframe : The DataFrame containing the data to check.
    column : The name of the column in the DataFrame whose values should be checked.
    catalog : The list (catalog) containing the allowed values.

    Exceptions:
    -----------
    ValueError: Raised if the column does not exist in the DataFrame or if the catalog is empty.

    Returns:
    -------
    bool:
        Returns True if all values in the column are found in the catalog.
        Returns False if any value is not found in the catalog.
    """

    if column not in dataframe.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")

    if not catalog:
        raise ValueError("The catalog is empty.")

    values_in_catalog = dataframe[column].isin(catalog)

    if values_in_catalog.all():
        return True
    else:
        return False
