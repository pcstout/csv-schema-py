from .base_column import BaseColumn
from .column_types import ColumnTypes
from .config_property import ConfigProperty


class EnumColumn(BaseColumn):
    COLUMN_TYPE = ColumnTypes.ENUM

    def __init__(self, name=None, required=True, null_or_empty=False, values=ConfigProperty.NotSpecified()):
        super(EnumColumn, self).__init__(self.COLUMN_TYPE, name, required, null_or_empty)

        self.values = self.register_property(
            ConfigProperty('values', values, 'Fixed set of constants.', default=list)
        )

    def on_validate(self):
        """Validates that each property has the correct value/type.

        Returns:
            List of error messages or an empty list.
        """
        errors = super(EnumColumn, self).on_validate()

        is_list = isinstance(self.values.value, list)

        if not is_list:
            errors.append('"values" must be a list.')

        if is_list and len(self.values.value) == 0:
            errors.append('"values" must contain at least one value.')

        return errors

    def on_validate_value(self, row_number, value):
        errors = []

        if (value is None or len(value.strip()) == 0) and self.null_or_empty.value is True:
            # Null/empty values are allowed.
            pass
        elif value is not None and value not in self.values.value:
            self.add_value_error(errors, row_number, value,
                                 'must be one of: "{0}"'.format(','.join(self.values.value)))

        return errors
