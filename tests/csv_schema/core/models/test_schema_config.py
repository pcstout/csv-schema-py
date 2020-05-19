import pytest
import os
import json
from src.csv_schema.core.models import SchemaConfig, SchemaConfigFilename, StringColumn


@pytest.fixture
def config_path(mk_tempfile):
    return mk_tempfile(suffix='.json')


@pytest.fixture
def empty_config(config_path):
    return SchemaConfig(config_path)


@pytest.fixture
def complete_config(config_path):
    columns = [
        StringColumn('col1', True, False, '', 0, 255),
        StringColumn('col2', True, False, '', 0, 255)
    ]
    sc = SchemaConfig(config_path,
                      name='Complete Config',
                      description='A Description',
                      columns=columns)

    return sc


def test_it_has_the_properties(empty_config, config_path):
    assert empty_config.path == os.path.abspath(config_path)

    assert len(empty_config.properties) == 4

    assert hasattr(empty_config, 'name')
    assert empty_config.name.value is None

    assert hasattr(empty_config, 'description')
    assert empty_config.description.value is None

    assert hasattr(empty_config, 'filename')
    assert isinstance(empty_config.filename.value, SchemaConfigFilename)

    assert hasattr(empty_config, 'columns')
    assert isinstance(empty_config.columns.value, list)
    assert len(empty_config.columns.value) == 0


def test_on_validate(empty_config):
    assert empty_config.is_valid() is False
    errors = empty_config.validate()
    assert '"name" must be specified.' in errors
    assert '"columns" must have at least one item.' in errors

    empty_config.filename.value = object()
    errors = empty_config.validate()
    assert '"filename" must be of type: SchemaConfigFilename' in errors
    empty_config.filename.clear()

    empty_config.name.value = 'test'
    errors = empty_config.validate()
    assert '"name" must be specified.' not in errors

    empty_config.columns.value.append(StringColumn('col1'))
    errors = empty_config.validate()
    assert '"columns" must have at least one item.' not in errors
    assert len(errors) == 0

    # Child ConfigObjects in lists are validated.
    empty_config.columns.value.append(StringColumn(None))
    errors = empty_config.validate()
    assert '"columns" -> "name" must be specified.' in errors
    assert len(errors) == 1


def test_save(complete_config):
    assert complete_config.save() == complete_config

    with open(complete_config.path) as f:
        json_data = json.load(f)
    assert complete_config.to_dict() == json_data


def test_load(complete_config):
    complete_config.save()
    new_config = SchemaConfig(complete_config.path).load()
    assert new_config.to_dict() == complete_config.to_dict()
    assert new_config.to_json() == complete_config.to_json()
