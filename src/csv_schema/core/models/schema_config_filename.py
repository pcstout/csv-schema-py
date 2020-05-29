from .base_config_object import BaseConfigObject
from .config_property import ConfigProperty


class SchemaConfigFilename(BaseConfigObject):

    def __init__(self, regex=None):
        super(SchemaConfigFilename, self).__init__()
        self.regex = self.register_property(
            ConfigProperty('regex', regex, 'Regular expression to validate the name of the CSV file being validated.')
        )
