from assertpy import assert_that
from tests.global_test_data import df_global
from data_quality_kit.consistency import assert_that_columns_values_match
from data_quality_kit.consistency import assert_that_there_are_not_duplicates


def test_assert_that_columns_values_match_successful():
    df1 = df_global[['match_column1']].copy()
    df2 = df_global[['match_column2']].copy()
    assert_that(assert_that_columns_values_match(
        df1, 'match_column1', df2, 'match_column2')).is_true()


def test_assert_that_columns_values_match_with_duplicates():
    df1 = df_global[['match_column1']].copy()
    df2 = df_global[['match_column_with_duplicates']].copy()
    assert_that(assert_that_columns_values_match(df1, 'match_column1',
                df2, 'match_column_with_duplicates')).is_true()


def test_assert_that_columns_values_not_match():
    df1 = df_global[['match_column1']].copy()
    df2 = df_global[['unique_ids']].copy()
    assert_that(assert_that_columns_values_match(
        df1, 'match_column1', df2, 'unique_ids')).is_false()


def test_assert_that_columns_values_match_with_invalid_column_in_first_df():
    error_msg = 'Error: The column "nonexistent" does not exist in the first DataFrame.'
    assert_that(assert_that_columns_values_match).raises(ValueError).when_called_with(
        df_global[['match_column1']], 'nonexistent', df_global[['match_column2']], 'match_column2'
    ).is_equal_to(error_msg)


def test_assert_that_columns_values_match_with_invalid_column_in_second_df():
    error_msg = 'Error: The column "nonexistent" does not exist in the second DataFrame.'
    assert_that(assert_that_columns_values_match).raises(ValueError).when_called_with(
        df_global[['match_column1']], 'match_column1', df_global[['match_column2']], 'nonexistent'
    ).is_equal_to(error_msg)


def test_assert_that_there_are_duplicates_invalid_case():
    assert_that(assert_that_there_are_not_duplicates(df_global, 'unique_ids')).is_false()


def test_assert_that_there_are_not_duplicates_valid_case():
    assert_that(assert_that_there_are_not_duplicates(df_global, 'duplicated_ids')).is_true()


def test_assert_that_there_are_not_duplicates_with_invalid_column_name():
    error_msg = 'Column "nonexistent" not in DataFrame.'
    assert_that(assert_that_there_are_not_duplicates).raises(ValueError).when_called_with(
        df_global, "nonexistent"
    ).is_equal_to(error_msg)
