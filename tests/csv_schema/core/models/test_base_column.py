import pytest
import json
from src.csv_schema.core.models import BaseColumn, ColumnTypes, ConfigProperty


@pytest.fixture
def col_type():
    return ColumnTypes.STRING


@pytest.fixture
def col_name():
    return 'test_col_a'


@pytest.fixture
def col_required():
    return True


@pytest.fixture
def col_null_or_empty():
    return False


@pytest.fixture
def col(col_type, col_name, col_required, col_null_or_empty):
    return BaseColumn(col_type, col_name, col_required, col_null_or_empty)


def test_it_sets_the_column_data(col_type, col_name, col_required, col_null_or_empty, col):
    assert col.name.value == col_name
    assert col.required.value == col_required
    assert col.null_or_empty.value == col_null_or_empty


def test_register_property(col):
    col.properties.clear()
    prop = ConfigProperty('test', None, '')

    # Adds it and returns it.
    assert col.register_property(prop) == prop
    assert prop in col.properties

    # Does not duplicate it.
    col.register_property(prop)
    assert prop in col.properties
    assert len(col.properties) == 1


def test_to_dict(col_type, col_name, col_required, col_null_or_empty, col):
    d = col.to_dict()
    assert len(d) == 4
    assert d['type'] == col_type
    assert d['name'] == col_name
    assert d['required'] == col_required
    assert d['null_or_empty'] == col_null_or_empty


def test_to_json(col):
    d = col.to_dict()
    j = col.to_json()
    assert json.loads(j) == d


def test_to_md_help(col_type, col_name, col_required, col_null_or_empty, col):
    # TODO: How to test this?
    print(col.to_md_help())


def test_validate_value_must_be_string():
    col = BaseColumn(name='col1')

    for string_value in ['a', '1']:
        errors = col.validate_value(1, string_value)
        assert not errors

    for non_string_value in [0, 1, 0.00, object()]:
        with pytest.raises(ValueError) as ex:
            col.validate_value(1, non_string_value)
        assert str(ex.value) == 'value must be a string.'


def test_validate_value_null_or_empty():
    col = BaseColumn(name='col1', null_or_empty=False)
    empty_values = ['', '  ']

    for empty_value in empty_values:
        errors = col.validate_value(1, empty_value)
        assert errors
        assert 'cannot be null or empty' in errors[0]

    col.null_or_empty.value = True
    for empty_value in empty_values:
        errors = col.validate_value(1, empty_value)
        assert not errors


def test_add_value_error(col, col_name):
    errors = []
    col.add_value_error(errors, 9, 'a', 'ERROR_STR1')
    assert errors[0] == 'Row number: 9, column: "{0}", value: "a" ERROR_STR1.'.format(col_name)
    col.add_value_error(errors, 9, 'a', 'ERROR_STR2')
    assert errors[1] == 'Row number: 9, column: "{0}", value: "a" ERROR_STR2.'.format(col_name)
