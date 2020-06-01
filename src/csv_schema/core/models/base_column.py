from .base_config_object import BaseConfigObject
from .column_types import ColumnTypes
from .config_property import ConfigProperty


class BaseColumn(BaseConfigObject):
    def __init__(self, type=None, name=None, required=None, null_or_empty=None):
        super(BaseColumn, self).__init__()

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

    def on_validate(self):
        """Validates that each property has the correct value/type.

        Returns:
            List of error messages or an empty list.
        """
        errors = super(BaseColumn, self).on_validate()

        if self.type.value not in ColumnTypes.ALL:
            errors.append('"type" must be one of: {0}'.format(','.join(ColumnTypes.ALL)))

        if self.name.value is None or len(self.name.value.strip()) == 0:
            errors.append('"name" must be specified.')

        if self.required.value not in [True, False]:
            errors.append('"required" must be True or False.')

        if self.null_or_empty.value not in [True, False]:
            errors.append('"null_or_empty" must be True or False.')

        return errors

    def validate_value(self, row_number, value):
        """Validates the value for a column from a CSV file.

        Args:
            row_number: The row number the value belongs to in the CSV file.
            value: The column value from the CSV file. This should always be a string.

        Returns:
            List of error messages or an empty list.
        """
        errors = []

        if not isinstance(value, str):
            raise ValueError('value must be a string.')

        if self.null_or_empty.value is False:
            if value is None or len(str(value).strip()) == 0:
                errors.append('Row number: {0}, column: "{1}", value: "{2}" cannot be null or empty.".'.format(
                    row_number,
                    self.name.value,
                    value)
                )

        sub_errors = self.on_validate_value(row_number, value)
        if sub_errors:
            errors += sub_errors

        return errors

    def on_validate_value(self, row_number, value):
        """Override to implement value validation in sub-classes.

        Returns:
            List of error messages or an empty list.
        """
        return []

    def add_value_error(self, errors, row_number, value, error):
        errors.append(
            'Row number: {0}, column: "{1}", value: "{2}" {3}.'.format(
                row_number,
                self.name.value,
                value,
                error)
        )
