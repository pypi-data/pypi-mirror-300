from assertpy import assert_that

from tests.global_test_data import df_global

from data_quality_kit.accuracy import assert_that_type_value, assert_that_values_in_catalog


def test_assert_that_type_value_correct():
    assert_that(assert_that_type_value(df_global, 'column1', int)).is_true()
    assert_that(assert_that_type_value(df_global, 'column3', str)).is_true()


def test_assert_that_type_value_incorrect():
    assert_that(assert_that_type_value(df_global, 'column3', int)).is_false()
    assert_that(assert_that_type_value(df_global, 'column2', str)).is_false()


def test_assert_that_type_value_in_nonexistent_column():
    error_msg = 'Column "nonexistent" not in DataFrame.'
    assert_that(assert_that_type_value).raises(ValueError).when_called_with(
        df_global, "nonexistent", int
    ).is_equal_to(error_msg)


def test_assert_that_values_in_catalog_with_all_values_in_catalog():
    catalog = ['Value1', 'Value2', 'Value3', 'Value4']
    result = assert_that_values_in_catalog(df_global, 'test_column', catalog)
    assert_that(result).is_true()


def test_assert_that_values_in_catalog_with_not_all_values_in_catalog():
    catalog = ['Value1', 'Value2', 'Value3']
    result = assert_that_values_in_catalog(df_global, 'test_column', catalog)
    assert_that(result).is_false()


def test_assert_that_values_in_catalog_with_column_not_in_dataframe():
    error_msg = "Column 'non_existent_column' does not exist in the DataFrame."
    assert_that(assert_that_values_in_catalog).raises(ValueError).when_called_with(
        df_global, 'non_existent_column', ['Value1', 'Value2']
    ).is_equal_to(error_msg)


def test_assert_that_values_in_catalog_with_empty_catalog():
    error_msg = "The catalog is empty."
    assert_that(assert_that_values_in_catalog).raises(ValueError).when_called_with(
        df_global, 'test_column', []
    ).is_equal_to(error_msg)
