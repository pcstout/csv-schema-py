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
