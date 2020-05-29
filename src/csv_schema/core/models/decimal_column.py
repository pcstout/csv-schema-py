import decimal as dec
import re
from locale import localeconv
from .base_column import BaseColumn
from .column_types import ColumnTypes
from .config_property import ConfigProperty


class DecimalColumn(BaseColumn):
    COLUMN_TYPE = ColumnTypes.DECIMAL

    def __init__(self, name=None, required=True, null_or_empty=False, regex=None, min=None, max=None, precision=2):
        super(DecimalColumn, self).__init__(self.COLUMN_TYPE, name, required, null_or_empty)

        self.regex = self.register_property(
            ConfigProperty('regex', regex, 'Regular expression to validate the column value.')
        )
        self.min = self.register_property(
            ConfigProperty('min', min, 'The minimum value. null for no limit.')
        )
        self.max = self.register_property(
            ConfigProperty('max', max, 'The maximum value. null for no limit.')
        )
        self.precision = self.register_property(
            ConfigProperty('precision', precision, 'The decimal point precision.')
        )

    def on_validate(self):
        """Validates that each property has the correct value/type.

        Returns:
            List of error messages or an empty list.
        """
        errors = super(DecimalColumn, self).on_validate()

        if self.regex.value is not None and not isinstance(self.regex.value, str):
            errors.append('"regex" must be a string.')

        min_set = self.min.value is not None
        min_is_number = isinstance(self.min.value, int) or \
                        isinstance(self.min.value, float) or \
                        isinstance(self.min.value, dec.Decimal)
        if min_set and not min_is_number:
            errors.append('"min" must be a number.')

        max_set = self.max.value is not None
        max_is_number = isinstance(self.max.value, int) or \
                        isinstance(self.max.value, float) or \
                        isinstance(self.max.value, dec.Decimal)
        if max_set and not max_is_number:
            errors.append('"max" must be a number.')

        if min_is_number and max_is_number:
            if self.min.value > self.max.value:
                errors.append('"min" must be less than or equal to "max".')
            if self.max.value < self.min.value:
                errors.append('"max" must be greater than or equal to "min".')

        if self.precision.value is not None:
            if not isinstance(self.precision.value, int):
                errors.append('"precision" must be an integer.')
            else:
                if self.precision.value < 1:
                    errors.append('"precision" must be greater than or equal to 1.')

        return errors

    def on_validate_value(self, row_number, value):
        errors = []
        decimal_value = None

        if re.search(r'^[-+]?\d*[.,]\d*$', value) is not None:
            decimal_value = dec.Decimal(value)
        elif len(value.strip()) == 0:
            # If the value is an empty string then convert it to None.
            value = None

        if value is not None and decimal_value is None:
            self.add_value_error(errors, row_number, value,
                                 'must be a decimal')

        if self.regex.value and not re.search(self.regex.value, value) is not None:
            self.add_value_error(errors, row_number, value,
                                 'does not match regex: "{0}"'.format(self.regex.value))

        if self.min.value is not None and decimal_value is not None and decimal_value < self.min.value:
            self.add_value_error(errors, row_number, value,
                                 'must be greater than or equal to: "{0}"'.format(self.min.value))

        if self.max.value is not None and decimal_value is not None and decimal_value > self.max.value:
            self.add_value_error(errors, row_number, value,
                                 'must be less than or equal to: "{0}"'.format(self.max.value))

        if self.precision.value is not None and decimal_value is not None:
            decimal_char = localeconv()['decimal_point']
            count = value[::-1].find(decimal_char)
            if count != self.precision.value:
                self.add_value_error(errors, row_number, value,
                                     'precision must be: "{0}"'.format(self.precision.value))

        return errors
