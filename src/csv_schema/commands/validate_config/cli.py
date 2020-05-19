import sys
from .validate_config import ValidateConfig
from ...core import ExitCodes


def create(subparsers, parents):
    parser = subparsers.add_parser('validate-config',
                                   parents=parents,
                                   help='Validates the CSV schema JSON configuration file.')
    parser.add_argument('schema', help='The JSON file to validate.')
    parser.set_defaults(_execute=execute)


def execute(args):
    vc = ValidateConfig(args.schema)
    vc.execute()
    if len(vc.errors) > 0:
        sys.exit(ExitCodes.FAIL)
    else:
        sys.exit(ExitCodes.SUCCESS)
