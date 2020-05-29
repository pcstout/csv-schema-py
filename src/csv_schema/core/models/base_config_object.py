import os
import json
from .column_types import ColumnTypes


class BaseConfigObject(object):
    def __init__(self):
        self.properties = []

    def register_property(self, prop):
        """Registers a configuration property.

        Args:
            prop: The ConfigProperty to register.

        Returns:
            The registered ConfigProperty.
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
        errors = self.on_validate()
        for prop in self.properties:
            if isinstance(prop.value, BaseConfigObject):
                child_errors = prop.value.validate()
                for child_error in child_errors:
                    errors.append('"{0}" -> {1}'.format(prop.name, child_error))
            elif isinstance(prop.value, list):
                for item in prop.value:
                    if isinstance(item, BaseConfigObject):
                        item_errors = item.validate()
                        for item_error in item_errors:
                            errors.append('"{0}" -> {1}'.format(prop.name, item_error))

        return errors

    def on_validate(self):
        """Override to implement validation in sub-classes.

        Returns:
            List of error messages or an empty list.
        """
        return []

    def clear(self):
        """Clear all the config property values and reset to their defaults.

        Returns:
            None
        """
        for prop in self.properties:
            prop.clear()

    def to_dict(self):
        """Gets the config properties as a dict.

        Returns:
            Config properties as a dict.
        """
        result = {}
        for prop in self.properties:
            if isinstance(prop.value, BaseConfigObject):
                result[prop.name] = prop.value.to_dict()
            elif isinstance(prop.value, list):
                result[prop.name] = []
                for item in prop.value:
                    if isinstance(item, BaseConfigObject):
                        result[prop.name].append(item.to_dict())
                    else:
                        result[prop.name].append(item)
            else:
                result[prop.name] = prop.value

        return result

    def to_json(self):
        """Gets the config properties as JSON.

        Returns:
            Config properties as JSON
        """
        return json.dumps(self.to_dict(), indent=2)

    def from_json(self, json_data):
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        for prop in self.properties:
            if prop.name not in json_data:
                raise KeyError(prop.name)

            json_value = json_data.get(prop.name)

            if isinstance(prop.value, BaseConfigObject):
                prop.value.from_json(json_value)
            elif isinstance(prop.value, list) and isinstance(json_value, list):
                prop.clear()
                for item in json_value:
                    # List items can only be of a certain type, figure out which one it is.
                    # Only Columns are supported right now.
                    if 'type' in item and 'name' in item and 'required' in item and 'null_or_empty' in item:
                        list_item = ColumnTypes.get_instance(item['type'])
                        list_item.from_json(item)
                        prop.value.append(list_item)
                    else:
                        prop.value.append(item)
            else:
                setattr(prop, 'value', json_value)
        return self

    def to_md_help(self):
        """Gets the help information for the config properties.

        Returns:
            String as markdown.
        """
        lines = []
        lines.append('```json')
        lines.append(self.to_json())
        lines.append('```')

        lines.append('| Property | Description |')
        lines.append('| -------- | ----------- |')

        child_configs = {}

        for prop in self.properties:
            lines.append('| {0} | {1} |'.format(prop.name, prop.description))
            if isinstance(prop.value, BaseConfigObject):
                child_configs[prop.name] = prop.value

        for child_name, child_value in child_configs.items():
            lines.append(os.linesep)
            lines.append('### {0}'.format(child_name))
            lines.append(child_value.to_md_help())

        return os.linesep.join(lines)
