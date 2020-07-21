class ColumnTypes:
    """Defines constants for all the column types."""

    STRING = 'string'
    INTEGER = 'integer'
    DECIMAL = 'decimal'
    ENUM = 'enum'
    ALL = [STRING, INTEGER, DECIMAL, ENUM]

    @classmethod
    def get_instance(cls, type_str):
        # Load column class on-demand to avoid circular dependency errors.
        # TODO: Refactor this?
        from .string_column import StringColumn
        from .integer_column import IntegerColumn
        from .decimal_column import DecimalColumn
        from .enum_column import EnumColumn
        if type_str == cls.STRING:
            return StringColumn()
        elif type_str == cls.INTEGER:
            return IntegerColumn()
        elif type_str == cls.DECIMAL:
            return DecimalColumn()
        elif type_str == cls.ENUM:
            return EnumColumn()
        else:
            raise ValueError('Invalid type: {0}'.format(type_str))
