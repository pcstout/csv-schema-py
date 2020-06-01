import pytest
from src.csv_schema.cli import main


def expect_exit_code(code, args):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(['generate-config'] + args)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == code


def test_it_passes(mk_tempdir):
    expect_exit_code(0, [mk_tempdir()])


def test_it_passes_with_csv(mk_tempdir):
    expect_exit_code(0, [mk_tempdir(), '--with-csv'])


def test_it_fails(mk_tempdir, mocker):
    mocker.patch('src.csv_schema.core.models.schema_config.SchemaConfig.validate', return_value=['test error'])
    expect_exit_code(1, [mk_tempdir()])
