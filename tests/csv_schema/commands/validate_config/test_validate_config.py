import pytest
from src.csv_schema.commands.validate_config import ValidateConfig


def test_it_passes_validation(valid_config_path):
    vc = ValidateConfig(valid_config_path)
    vc.execute()
    assert len(vc.errors) == 0


def test_it_does_not_pass_validation(invalid_config_path):
    vc = ValidateConfig(invalid_config_path)
    vc.execute()
    assert len(vc.errors) == 1
