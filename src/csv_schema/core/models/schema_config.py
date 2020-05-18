import os
import json
from ..utils import Utils
from .base_config_object import BaseConfigObject
from .config_property import ConfigProperty
from .schema_config_filename import SchemaConfigFilename


class SchemaConfig(BaseConfigObject):
    def __init__(self, path):
        self.path = Utils.expand_path(path)
        self.name = self.register_property(
            ConfigProperty('name', None, 'The name of the schema.')
        )
        self.description = self.register_property(
            ConfigProperty('description', None, 'The description of the schema.')
        )
        self.filename = self.register_property(
            ConfigProperty('filename', SchemaConfigFilename(),
                           'Properties for the name of the CSV filename to validate.')
        )
        self.columns = self.register_property(
            ConfigProperty('columns', [], 'List of column definitions.')
        )

    def open(self):
        if not os.path.isfile(self.path):
            raise FileNotFoundError(self.path)

        with open(self.path) as f:
            self.from_json(json.load(f))
        self.validate()

    def on_validate(self):
        """Validates that each property has the correct value/type.

        Returns:
            List of error messages or an empty list.
        """
        errors = super(SchemaConfig, self).validate()

        if self.name.value is None or len(self.name.value.strip()) == 0:
            errors.append('"name" must be specified.')

        if self.columns is None or len(self.columns) == 0:
            errors.append('"columns" must have at least one item.')

        if self.filename is not None and not isinstance(self.filename, SchemaConfigFilename):
            errors.append('"filename" must be of type: SchemaConfigFilename')

        if self.filename is not None:
            filename_errors = self.filename.validate()
            if filename_errors:
                errors += filename_errors

        return errors
