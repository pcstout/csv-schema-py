import os
import re
from ...core import Utils
from ..validate_config import ValidateConfig


class ValidateCsv:

    def __init__(self, csv_path, schema_path):
        self.csv_path = Utils.expand_path(csv_path)
        self.schema_path = Utils.expand_path(schema_path)
        self.config = None
        self.errors = []

    def execute(self):
        validate_config = ValidateConfig(self.schema_path)
        self.errors = validate_config.execute()
        self.config = validate_config.config
        if not self.errors:
            self._validate_csv()
        return self.errors

    def _validate_csv(self):
        if not self._validate_filename():
            return

    def _validate_filename(self):
        filename = self.config.filename.value
        if filename is None:
            return True

        if filename.regex.value:
            regex = filename.regex.value
            csv_filename = os.path.basename(self.csv_path)
            is_valid = re.search(regex, csv_filename) is not None
            if not is_valid:
                self.errors.append('CSV file name: "{0}" does not match regex: "{1}"'.format(csv_filename, regex))
            return is_valid
        else:
            return True
