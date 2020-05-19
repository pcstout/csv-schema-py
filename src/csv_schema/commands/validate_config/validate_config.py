from ...core import Utils
from ...core.models import SchemaConfig


class ValidateConfig:
    def __init__(self, schema_filename):
        self.filename = Utils.expand_path(schema_filename)
        self.errors = []

    def execute(self):
        """Execute the validation.

        Returns:
            List of errors or empty list.
        """
        config = SchemaConfig(self.filename).load()
        self.errors = config.validate()
        if self.errors:
            print('Errors found in: {0}'.format(self.filename))
            for error in self.errors:
                print(error)
        else:
            print('No errors found in: {0}'.format(self.filename))
        return self.errors
