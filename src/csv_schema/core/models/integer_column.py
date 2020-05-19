from .base_column import BaseColumn
from .column_types import ColumnTypes
from .config_property import ConfigProperty


class IntegerColumn(BaseColumn):
    COLUMN_TYPE = ColumnTypes.INTEGER

    def __init__(self, name, required=True, null_or_empty=False, regex=None, min=None, max=None):
        super(IntegerColumn, self).__init__(self.COLUMN_TYPE, name, required, null_or_empty)

        self.regex = self.register_property(
            ConfigProperty('regex', regex, 'Regular expression to validate the column value.')
        )
        self.min = self.register_property(
            ConfigProperty('min', min, 'The minimum value. null for no limit.')
        )
        self.max = self.register_property(
            ConfigProperty('max', max, 'The maximum value. null for no limit.')
        )

    def on_validate(self):
        """Validates that each property has the correct value/type.

        Returns:
            List of error messages or an empty list.
        """
        errors = super(IntegerColumn, self).on_validate()

        if self.regex.value is not None and not isinstance(self.regex.value, str):
            errors.append('"regex" must be a string.')

        if self.min.value is not None and not isinstance(self.min.value, int):
            errors.append('"min" must be an integer.')

        if self.max.value is not None and not isinstance(self.max.value, int):
            errors.append('"max" must be an integer.')

        return errors
