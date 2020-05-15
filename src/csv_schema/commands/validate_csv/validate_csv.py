import os
import json
from ...core import Utils, AioManager


class ValidateCsv:

    def __init__(self, csv_filename, schema_filename):
        self.csv_filename = Utils.expand_path(csv_filename)
        self.schema_filename = Utils.expand_path(schema_filename)

    def execute(self):
        return AioManager.start(self._execute_async)

    async def _execute_async(self):
        # TODO:
        return self
