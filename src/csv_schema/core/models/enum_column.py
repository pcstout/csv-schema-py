from .base_column import BaseColumn
from .column_types import ColumnTypes
from .config_property import ConfigProperty


class EnumColumn(BaseColumn):
    COLUMN_TYPE = ColumnTypes.ENUM

    def __init__(self, name, required=True, null_or_empty=False, values=[]):
        super(EnumColumn, self).__init__(self.COLUMN_TYPE, name, required, null_or_empty)

        self.values = self.register_property(
            ConfigProperty('values', values, 'Fixed set of constants.')
        )

    def on_validate(self):
        """Validates that each property has the correct value/type.

        Returns:
            List of error messages or an empty list.
        """
        errors = super(EnumColumn, self).on_validate()

        if self.values.value is None:
            errors.append('"values" must contain at least one value.')

        if not isinstance(self.values.value, list):
            errors.append('"values" must be a list.')

        return errors
