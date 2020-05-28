import pytest
from src.csv_schema.core.models import EnumColumn


@pytest.fixture
def enum_values():
    return ['a', 'b', 'c']


@pytest.fixture
def col(enum_values):
    return EnumColumn(name='col1', values=enum_values)


def test_validate_value_must_be_string(col, enum_values):
    for string_value in enum_values:
        errors = col.validate_value(1, string_value)
        assert not errors

    for non_string_value in [0, 1, 0.00, object()]:
        with pytest.raises(ValueError) as ex:
            col.validate_value(1, non_string_value)
        assert str(ex.value) == 'value must be a string.'


def test_validate_value_null_or_empty(col):
    empty_values = ['', '  ']

    for empty_value in empty_values:
        errors = col.validate_value(1, empty_value)
        assert errors
        assert 'cannot be null or empty' in errors[0]

    col.null_or_empty.value = True
    for empty_value in empty_values:
        errors = col.validate_value(1, empty_value)
        assert not errors


def test_validate_value_must_be_one_of_values(col, enum_values):
    for valid_value in enum_values:
        errors = col.validate_value(1, valid_value)
        assert not errors

    for invalid_value in ['1', 'z']:
        errors = col.validate_value(1, invalid_value)
        assert errors
        assert 'must be one of' in errors[0]
