import pytest
from src.csv_schema.cli import main


def expect_exit_code(csv_path, config_path, code):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(['validate-csv', csv_path, config_path])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == code


def test_it_passes(valid_csv_path, valid_config_path):
    expect_exit_code(valid_csv_path, valid_config_path, 0)


def test_it_fails(invalid_csv_path, invalid_config_path):
    expect_exit_code(invalid_csv_path, invalid_config_path, 1)
