import pytest
from src.csv_schema.cli import main


def expect_exit_code(out_path, code):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(['generate-config', out_path])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == code


def test_it_passes(mk_tempdir):
    expect_exit_code(mk_tempdir(), 0)


def test_it_fails(mk_tempdir, mocker):
    mocker.patch('src.csv_schema.core.models.schema_config.SchemaConfig.validate', return_value=['test error'])
    expect_exit_code(mk_tempdir(), 1)
