import os
import json
from .column_types import ColumnTypes
from .config_property import ConfigProperty


class BaseColumn(object):
    def __init__(self, type, name, required, null_or_empty):
        self.properties = []

        self.type = self.register_property(
            ConfigProperty('type', type, 'The column type.')
        )
        self.name = self.register_property(
            ConfigProperty('name', name, 'The name of the column.')
        )
        self.required = self.register_property(
            ConfigProperty('required', required, 'Whether or not the column is required in the file.')
        )
        self.null_or_empty = self.register_property(
            ConfigProperty('null_or_empty', null_or_empty,
                           'Whether or not the value can be null (missing) or an empty string.')
        )

    def register_property(self, prop):
        """Registers a column property.

        Args:
            prop: The ColumnProperty to register.

        Returns:
            The registered ColumnProperty.
        """
        if prop not in self.properties:
            self.properties.append(prop)
        return prop

    def is_valid(self):
        """Get if the column data passes validation.

        Returns:
            True or False
        """
        return len(self.validate()) == 0

    def validate(self):
        """Validates that each property has the correct value/type.

        Returns:
            List of error messages or an empty list.
        """
        errors = []

        if self.type.value not in ColumnTypes.ALL:
            errors.append('"type" must be one of: {0}'.format(','.join(ColumnTypes.ALL)))

        if self.name.value is None or len(self.name.value.strip()) == 0:
            errors.append('"name" must be specified.')

        if self.required.value not in [True, False]:
            errors.append('"required" must be True or False.')

        if self.null_or_empty.value not in [True, False]:
            errors.append('"null_or_empty" must be True or False.')

        return errors

    def to_dict(self):
        """Gets the column properties as a dict.

        Returns:
            Column properties as a dict.
        """
        result = {}
        for prop in self.properties:
            result[prop.name] = prop.value

        return result

    def to_json(self):
        """Gets the column properties as JSON.

        Returns:
            Column properties as JSON
        """
        return json.dumps(self.to_dict(), indent=2)

    def to_md_help(self):
        """Gets the help information for the column.

        Returns:
            String as markdown.
        """
        lines = ['### {0}'.format(self.type)]
        lines.append('```json')
        lines.append(self.to_json())
        lines.append('```')

        lines.append('| Property | Description |')
        lines.append('| -------- | ----------- |')

        for prop in self.properties:
            lines.append('| {0} | {1} |'.format(prop.name, prop.description))

        return os.linesep.join(lines)
