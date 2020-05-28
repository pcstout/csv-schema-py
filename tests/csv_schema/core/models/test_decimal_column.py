import pytest
from src.csv_schema.core.models import DecimalColumn


def test_validate_value_must_be_string():
    col = DecimalColumn(name='col1')

    for string_value in ['0.00', '1.00']:
        errors = col.validate_value(1, string_value)
        assert not errors

    for non_string_value in [0, 1, 0.00, object()]:
        with pytest.raises(ValueError) as ex:
            col.validate_value(1, non_string_value)
        assert str(ex.value) == 'value must be a string.'


def test_validate_value_null_or_empty():
    col = DecimalColumn(name='col1', null_or_empty=False)
    empty_values = ['', '  ']

    for empty_value in empty_values:
        errors = col.validate_value(1, empty_value)
        assert errors
        assert 'cannot be null or empty' in errors[0]

    col.null_or_empty.value = True
    for empty_value in empty_values:
        errors = col.validate_value(1, empty_value)
        assert not errors


def test_validate_value_is_decimal():
    col = DecimalColumn(name='col1')

    for decimal_value in ['-9.00', '0.00', '9.00']:
        errors = col.validate_value(1, decimal_value)
        assert not errors

    for non_decimal_value in ['1', '1a', 'z']:
        errors = col.validate_value(1, non_decimal_value)
        assert errors
        assert 'must be a decimal' in errors[0]


def test_validate_value_regex():
    col = DecimalColumn(name='col1', regex='^[0-3].[0-3][0-3]$')

    for matching_value in ['0.00', '3.10']:
        errors = col.validate_value(1, matching_value)
        assert not errors

    for non_matching_value in ['10', 'a', 'z5']:
        errors = col.validate_value(1, non_matching_value)
        assert errors
        assert 'does not match regex' in errors[-1]


def test_validate_value_min():
    col = DecimalColumn(name='col1', min=3.5)

    for min_value in ['3.50', '5.10', '10.10', '1000.10']:
        errors = col.validate_value(1, min_value)
        assert not errors

    for non_min_value in ['3.40', '0.00', '-1.10', '-1000.10']:
        errors = col.validate_value(1, non_min_value)
        assert errors
        assert 'must be greater than or equal to' in errors[0]


def test_validate_value_max():
    col = DecimalColumn(name='col1', max=3.5)

    for max_value in ['-1000.00', '-1.00', '0.00', '1.10', '3.50']:
        errors = col.validate_value(1, max_value)
        assert not errors

    for non_max_value in ['3.60', '10.10', '1000.10']:
        errors = col.validate_value(1, non_max_value)
        assert errors
        assert 'must be less than or equal to' in errors[-1]


def test_validate_precision():
    col = DecimalColumn(name='col1', precision=1)
    errors = col.validate_value(1, '1.0')
    assert not errors

    col = DecimalColumn(name='col1', precision=2)
    errors = col.validate_value(1, '1.00')
    assert not errors

    for invalid_precision in ['1.0', '1.000']:
        errors = col.validate_value(1, invalid_precision)
        assert errors
        assert 'precision must be: "2"' in errors[0]
