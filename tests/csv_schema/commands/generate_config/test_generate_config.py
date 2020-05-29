import pytest
import os
from src.csv_schema.commands.generate_config import GenerateConfig
from src.csv_schema.core.models import ColumnTypes, SchemaConfig


def assert_success(gc):
    assert not gc.errors
    assert os.path.isfile(gc.path)
    found_types = [c.type.value for c in gc.config.columns.value]
    assert found_types == ColumnTypes.ALL
    loaded = SchemaConfig(gc.path).load()
    assert loaded.to_dict() == gc.config.to_dict()


def test_it_works(mk_tempdir):
    temp_dir = mk_tempdir()
    gc = GenerateConfig(temp_dir)
    gc.execute()
    assert_success(gc)


def test_it_adds_the_filename_for_dir_paths(mk_tempdir):
    temp_dir = mk_tempdir()
    gc = GenerateConfig(temp_dir)
    gc.execute()
    assert_success(gc)
    assert os.path.dirname(gc.path) == temp_dir
    assert os.path.basename(gc.path) == 'csv-schema.json'


def test_it_does_not_add_the_filename_for_file_paths(mk_tempfile):
    temp_dir = mk_tempfile(suffix=".JsOn")
    gc = GenerateConfig(temp_dir)
    gc.execute()
    assert_success(gc)
    assert gc.path == temp_dir
    assert os.path.basename(gc.path) == os.path.basename(temp_dir)


def test_it_creates_dirs(mk_tempdir):
    temp_dir = mk_tempdir()
    temp_path = os.path.join(temp_dir, 'dir1', 'dir2', 'dir3')
    gc = GenerateConfig(temp_path)
    gc.execute()
    assert_success(gc)
    assert os.path.dirname(gc.path) == temp_path
    assert os.path.basename(gc.path) == 'csv-schema.json'

    temp_path = os.path.join(temp_dir, 'dir1', 'dir2', 'dir3', 'test.json')
    gc = GenerateConfig(temp_path)
    gc.execute()
    assert_success(gc)
    assert os.path.dirname(gc.path) == os.path.dirname(temp_path)
    assert os.path.basename(gc.path) == 'test.json'
