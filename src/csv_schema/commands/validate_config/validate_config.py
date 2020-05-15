import os
import json
from ...core import Utils, AioManager


class ValidateConfig:
    def __init__(self, schema_filename):
        self.filename = Utils.expand_path(schema_filename)

    def execute(self):
        return AioManager.start(self._execute_async)

    async def _execute_async(self):
        # TODO:
        return self
