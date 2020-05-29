class ConfigProperty:
    class NotSpecified:
        pass

    def __init__(self, name, value=NotSpecified(), description=None, default=None):
        self.name = name
        self.value = value
        self.description = description
        self.default = default
        if isinstance(value, ConfigProperty.NotSpecified):
            self.clear()

    def clear(self):
        if isinstance(self.default, type):
            self.value = self.default()
        else:
            self.value = self.default
