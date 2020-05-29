import re
from .base_column import BaseColumn
from .column_types import ColumnTypes
from .config_property import ConfigProperty


class StringColumn(BaseColumn):
    COLUMN_TYPE = ColumnTypes.STRING

    def __init__(self, name=None, required=True, null_or_empty=False, regex=None, min=None, max=None):
        super(StringColumn, self).__init__(self.COLUMN_TYPE, name, required, null_or_empty)

        self.regex = self.register_property(
            ConfigProperty('regex', regex, 'Regular expression to validate the column value.')
        )
        self.min = self.register_property(
            ConfigProperty('min', min, 'The minimum length of the string. null for no limit.')
        )
        self.max = self.register_property(
            ConfigProperty('max', max, 'The maximum length of the string. null for no limit.')
        )

    def on_validate(self):
        """Validates that each property has the correct value/type.

        Returns:
            List of error messages or an empty list.
        """
        errors = super(StringColumn, self).on_validate()

        if self.regex.value is not None and not isinstance(self.regex.value, str):
            errors.append('"regex" must be a string.')

        min_set = self.min.value is not None
        min_is_int = isinstance(self.min.value, int)
        if min_set and not min_is_int:
            errors.append('"min" must be an integer.')

        max_set = self.max.value is not None
        max_is_int = isinstance(self.max.value, int)
        if max_set and not max_is_int:
            errors.append('"max" must be an integer.')

        if min_is_int and max_is_int:
            if self.min.value > self.max.value:
                errors.append('"min" must be less than or equal to "max".')
            if self.max.value < self.min.value:
                errors.append('"max" must be greater than or equal to "min".')

        return errors

    def on_validate_value(self, row_number, value):
        errors = []

        if self.regex.value and not re.search(self.regex.value, value) is not None:
            self.add_value_error(errors, row_number, value,
                                 'does not match regex: "{0}"'.format(self.regex.value))

        if self.min.value is not None and len(value) < self.min.value:
            self.add_value_error(errors, row_number, value,
                                 'must be greater than or equal to: "{0}"'.format(self.min.value))

        if self.max.value is not None and len(value) > self.max.value:
            self.add_value_error(errors, row_number, value,
                                 'must be less than or equal to: "{0}"'.format(self.max.value))

        return errors
