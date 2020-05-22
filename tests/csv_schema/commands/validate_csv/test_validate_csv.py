import pytest
import os
from src.csv_schema.commands.validate_csv import ValidateCsv


def test_it_validates_the_csv_filename(populated_config, mk_valid_csv):
    csv_path = mk_valid_csv('test.csv')

    # Incorrect path with no regex - should pass
    vc = ValidateCsv('/tmp/test.csvX', populated_config.path)
    vc.execute()
    assert vc.config.filename.value.regex.value is None
    assert len(vc.errors) == 0

    # Correct path with regex - should pass
    populated_config.filename.value.regex.value = '^test\.csv$'
    populated_config.save()
    vc = ValidateCsv(csv_path, populated_config.path)
    vc.execute()
    assert len(vc.errors) == 0

    # Incorrect path with with regex - should not pass
    vc = ValidateCsv(csv_path + 'X', populated_config.path)
    vc.execute()
    assert len(vc.errors) > 0
    assert 'does not match regex' in vc.errors[0]
