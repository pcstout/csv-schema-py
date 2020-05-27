import pytest
from src.csv_schema.core.models import StringColumn


def test_validate_value_is_string():
    col = StringColumn(name='col1')
    errors = col.validate_value(1, 1)
    assert errors
    assert 'must be a string' in errors[0]

    errors = col.validate_value(1, object())
    assert errors
    assert 'must be a string' in errors[0]

    col = StringColumn(name='col1', null_or_empty=True)
    errors = col.validate_value(1, '')
    assert not errors


def test_validate_value_regex():
    col = StringColumn(name='col1', regex='^[0-9]$')
    errors = col.validate_value(1, '1')
    assert not errors
    errors = col.validate_value(1, '10')
    assert errors
    assert 'does not match regex' in errors[0]


def test_validate_value_min():
    col = StringColumn(name='col1', min=2)
    errors = col.validate_value(1, 'aa')
    assert not errors
    errors = col.validate_value(1, 'a')
    assert errors
    assert 'must be greater than or equal to' in errors[0]


def test_validate_value_max():
    col = StringColumn(name='col1', max=2)
    errors = col.validate_value(1, 'aa')
    assert not errors
    errors = col.validate_value(1, 'aaa')
    assert errors
    assert 'must be less than or equal to' in errors[0]
