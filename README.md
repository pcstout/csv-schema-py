# CVS Schema Definition and Validation

## Install

```bash
pip install csv-schema
```

# Definition

The CSV file schema definition will be defined in a JSON file in the following format.

## File Definition:

```json
{
  "name": "The Schema Name",
  "description": "A description of the schema.",
  "filename": null,
  "columns": []
}
```
|Property|Value|Description|
|--------|--------|-----------|
| name | string | The name of the schema. |
| description | string | The description of the schema. |
| filename | `null`, object | Properties for the name of the CSV filename to validate. |
| columns | array | List of column definitions. |

### filename
```json
{
  "regex": null
}
```
|Property|Value|Description|
|--------|--------|-----------|
| regex | `null`, regex | Regular expression to validate the name of the CSV file being validated. |

## Column Definitions:

### String
```json
{
  "type": "string",
  "name": "",
  "required": true,
  "null_or_empty": false,
  "regex": null,
  "min": 0,
  "max": 999
}
```
|Property|Value|Description|
|--------|--------|-----------|
| type | `string` | The column type. |
| name | string | The name of the column. |
| required | `true`, `false` | Whether or not the column is required in the file. |
| null_or_empty | `true`, `false` | Whether or not the value can be null (missing) or an empty string. |
| regex | `null`, regex | Regular expression to validate the column value. |
| min | integer | The minimum length of the string. `null` for no limit. |
| max | integer | The maximum length of the string. `null` for no limit. |

### Integer
```json
{
  "type": "integer",
  "name": "",
  "required": true,
  "null_or_empty": false,
  "regex": null,
  "min": 0,
  "max": 999
}
```
|Property|Value|Description|
|--------|--------|-----------|
| type | `integer` | The column type. |
| name | string | The name of the column. |
| required | `true`, `false` | Whether or not the column is required in the file. |
| null_or_empty | `true`, `false` | Whether or not the value can be null (missing) or an empty string. |
| regex | `null`, regex | Regular expression to validate the column value. |
| min | integer | The minimum value. `null` for no limit. |
| max | integer | The maximum value. `null` for no limit. |

### Decimal
```json
{
  "type": "decimal",
  "name": "",
  "required": true,
  "null_or_empty": false,
  "regex": null,
  "min": 0.00,
  "max": 999.99,
  "precision": 2
}
```
|Property|Value|Description|
|--------|--------|-----------|
| type | `decimal` | The column type. |
| name | string | The name of the column. |
| required | `true`, `false` | Whether or not the column is required in the file. |
| null_or_empty | `true`, `false` | Whether or not the value can be null (missing) or an empty string. |
| regex | `null`, regex | Regular expression to validate the column value. |
| min | integer | The minimum value. `null` for no limit. |
| max | integer | The maximum value. `null` for no limit. |
| precision| integer | The decimal point precision. |

### Enum
```json
{
  "type": "enum",
  "name": "",
  "required": true,
  "null_or_empty": false,
  "values": ["A", "B", "C"]
}
```
|Property|Value|Description|
|--------|--------|-----------|
| type | `enum` | The column type. |
| name | string | The name of the column. |
| required | `true`, `false` | Whether or not the column is required in the file. |
| null_or_empty | `true`, `false` | Whether or not the value can be null (missing) or an empty string. |
| values | array | Fixed set of constants. |

## Development Setup

```bash
pipenv --three
pipenv shell
make pip_install
make build
make install_local
```
See [Makefile](Makefile) for all commands.

### Testing

- Create and activate a virtual environment:
- Run the tests: `make test`
