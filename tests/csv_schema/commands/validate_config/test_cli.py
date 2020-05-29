import pytest
from src.csv_schema.cli import main


def expect_exit_code(config_path, code):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(['validate-config', config_path])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == code


def test_it_passes(valid_config_path):
    expect_exit_code(valid_config_path, 0)


def test_it_fails(invalid_config_path):
    expect_exit_code(invalid_config_path, 1)
