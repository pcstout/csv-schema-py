import os
from ...core import Utils
from ...core.models import SchemaConfig, ColumnTypes


class GenerateConfig:
    def __init__(self, path):
        self.path = Utils.expand_path(path)
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

        return self.errors
