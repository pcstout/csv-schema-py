import pytest
from src.csv_schema.core.models import StringColumn


def test_validate_value_must_be_string():
    col = StringColumn(name='col1')

    for string_value in ['a', 'abc']:
        errors = col.validate_value(1, string_value)
        assert not errors

    for non_string_value in [0, 1, 0.00, object()]:
        with pytest.raises(ValueError) as ex:
            col.validate_value(1, non_string_value)
        assert str(ex.value) == 'value must be a string.'


def test_validate_value_null_or_empty():
    col = StringColumn(name='col1', null_or_empty=False)
    empty_values = ['', '  ']

    for empty_value in empty_values:
        errors = col.validate_value(1, empty_value)
        assert errors
        assert 'cannot be null or empty' in errors[0]

    col.null_or_empty.value = True
    for empty_value in empty_values:
        errors = col.validate_value(1, empty_value)
        assert not errors


def test_validate_value_regex():
    col = StringColumn(name='col1', regex='^[a-c]$')

    for matching_value in ['a', 'b', 'c']:
        errors = col.validate_value(1, matching_value)
        assert not errors

    for non_matching_value in ['d', 'e', 'f', '0', '1']:
        errors = col.validate_value(1, non_matching_value)
        assert errors
        assert 'does not match regex' in errors[0]


def test_validate_value_min():
    col = StringColumn(name='col1', min=3)

    for min_value in ['aaa', 'aaaa']:
        errors = col.validate_value(1, min_value)
        assert not errors

    for non_min_value in ['a', 'aa']:
        errors = col.validate_value(1, non_min_value)
        assert errors
        assert 'must be greater than or equal to' in errors[0]


def test_validate_value_max():
    col = StringColumn(name='col1', max=3)

    for max_value in ['a', 'aa', 'aaa']:
        errors = col.validate_value(1, max_value)
        assert not errors

    for non_max_value in ['aaaa', 'aaaaaa']:
        errors = col.validate_value(1, non_max_value)
        assert errors
        assert 'must be less than or equal to' in errors[0]
