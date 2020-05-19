import os
import json
import aiofiles
from ..aio_manager import AioManager
from ..utils import Utils
from .base_config_object import BaseConfigObject
from .config_property import ConfigProperty
from .schema_config_filename import SchemaConfigFilename


class SchemaConfig(BaseConfigObject):

    def __init__(self, path, name=None, description=None, columns=[]):
        super(SchemaConfig, self).__init__()

        self.path = Utils.expand_path(path)
        self.name = self.register_property(
            ConfigProperty('name', name, 'The name of the schema.')
        )
        self.description = self.register_property(
            ConfigProperty('description', description, 'The description of the schema.')
        )
        self.filename = self.register_property(
            ConfigProperty('filename', SchemaConfigFilename(),
                           'Properties for the name of the CSV filename to validate.')
        )
        self.columns = self.register_property(
            ConfigProperty('columns', columns, 'List of column definitions.')
        )

    def load(self):
        """Loads a JSON file from self.path into self.

        Returns:
            Self
        """
        if not os.path.isfile(self.path):
            raise FileNotFoundError(self.path)

        self.from_json(AioManager.start(self._load_async))
        return self

    async def _load_async(self):
        async with aiofiles.open(self.path, mode='r') as f:
            data = await f.read()
            return json.loads(data)

    def save(self):
        """Saves self as JSON to self.path.

        Returns:
            Self
        """
        AioManager.start(self._save_async)
        # with open(self.path, 'w') as f:
        #     json.dump(self.to_dict(), f, indent=2)
        return self

    async def _save_async(self):
        async with aiofiles.open(self.path, mode='w') as f:
            # NOTE: json.dump is not working with aiofiles so do it this way.
            json_data = json.dumps(self.to_dict(), indent=2)
            await f.write(json_data)

    def on_validate(self):
        """Validates that each property has the correct value/type.

        Returns:
            List of error messages or an empty list.
        """
        errors = []

        if self.name.value is None or len(self.name.value.strip()) == 0:
            errors.append('"name" must be specified.')

        if self.columns.value is None or len(self.columns.value) == 0:
            errors.append('"columns" must have at least one item.')

        if self.filename.value is not None and not isinstance(self.filename.value, SchemaConfigFilename):
            errors.append('"filename" must be of type: SchemaConfigFilename')

        return errors
