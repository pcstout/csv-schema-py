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
        print('Errors found in: {0}'.format(vc.filename))
        for error in vc.errors:
            print(error)
        sys.exit(ExitCodes.FAIL)
    else:
        print('No errors found in: {0}'.format(vc.filename))
        sys.exit(ExitCodes.SUCCESS)
