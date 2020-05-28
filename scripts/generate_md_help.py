#!/usr/bin/env python3
# This script will generate markdown help for the README.md.
import os
import sys

script_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(script_dir, '..'))
import src.csv_schema.core.models as models

config = models.SchemaConfig('.')

markdown = '## File Definition:' + os.linesep
markdown = markdown + os.linesep + config.to_md_help() + os.linesep

markdown = markdown + os.linesep + '## Column Definitions:' + os.linesep

for column in [models.StringColumn(), models.IntegerColumn(), models.DecimalColumn(), models.EnumColumn()]:
    markdown = markdown + os.linesep + '### {0}'.format(column.type.value)
    markdown = markdown + os.linesep + column.to_md_help() + os.linesep

print(markdown)
