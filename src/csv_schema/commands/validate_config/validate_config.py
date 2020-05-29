from ...core import Utils
from ...core.models import SchemaConfig


class ValidateConfig:
    def __init__(self, schema_filename):
        self.filename = Utils.expand_path(schema_filename)
        self.config = None
        self.errors = []

    def execute(self):
        """Execute the validation.

        Returns:
            List of errors or empty list.
        """
        self.config = SchemaConfig(self.filename).load()
        self.errors = self.config.validate()
        return self.errors
