import os
import re
import csv
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
        if not self._validate_columns():
            return
        self._validate_data()

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

    def _validate_columns(self):
        with open(self.csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            headers = reader.fieldnames
            for column in self.config.columns.value:
                if column.required.value is True and column.name.value not in headers:
                    self.errors.append('Required column: "{0}" not found.'.format(column.name.value))
        return len(self.errors) == 0

    def _validate_data(self):
        with open(self.csv_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            row_number = 1
            for row in reader:
                for column in self.config.columns.value:
                    col_value = row[column.name.value]
                    errors = column.validate_value(row_number, col_value)
                    if errors:
                        self.errors += errors
                row_number += 1
        return len(self.errors) == 0
