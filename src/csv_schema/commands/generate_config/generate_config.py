import os
import csv
import random
from ...core import Utils
from ...core.models import SchemaConfig, ColumnTypes


class GenerateConfig:
    def __init__(self, path, with_csv=False, with_csv_rows=100):
        self.path = Utils.expand_path(path)
        self.with_csv = with_csv
        self.with_csv_rows = with_csv_rows
        self.csv_path = None
        self.config = None
        self.errors = []

    def execute(self):
        """Execute the generation.

        Returns:
            List of errors or empty list.
        """
        if os.path.isdir(self.path) or not self.path.lower().endswith('.json'):
            self.path = os.path.join(self.path, 'csv-schema.json')

        Utils.ensure_dirs(os.path.dirname(self.path))

        self.config = SchemaConfig(self.path)
        self.config.name.value = 'CSV Schema'
        self.config.description.value = 'Generated CSV Configuration.'

        count = 1
        for column_type in ColumnTypes.ALL:
            column = ColumnTypes.get_instance(column_type)
            column.name.value = 'col_{0}'.format(count)

            if column_type == ColumnTypes.ENUM:
                column.values.value = ['a', 'b', 'c']

            self.config.columns.value.append(column)
            count += 1

        self.errors = self.config.validate()
        if not self.errors:
            self.config.save()

        if self.with_csv:
            self._generate_test_csv()

        return self.errors

    def _generate_test_csv(self):
        self.csv_path = self.config.path + '.csv'
        with open(self.csv_path, mode='w', newline='') as f:
            csv_writer = csv.DictWriter(f, fieldnames=[c.name.value for c in self.config.columns.value])
            csv_writer.writeheader()
            row_count = 1
            while row_count <= self.with_csv_rows:
                row = {}
                for col in self.config.columns.value:
                    if col.type.value == ColumnTypes.STRING:
                        row[col.name.value] = 'string column value row {0}'.format(row_count)
                    elif col.type.value == ColumnTypes.INTEGER:
                        row[col.name.value] = row_count
                    elif col.type.value == ColumnTypes.DECIMAL:
                        row[col.name.value] = '{0}.{1}'.format(row_count, random.randint(10, 99))
                    elif col.type.value == ColumnTypes.ENUM:
                        row[col.name.value] = col.values.value[random.randint(0, 2)]
                csv_writer.writerow(row)
                row_count += 1
