import sys
from .generate_config import GenerateConfig
from ...core import ExitCodes


def create(subparsers, parents):
    parser = subparsers.add_parser('generate-config',
                                   parents=parents,
                                   help='Generate a CSV schema JSON configuration file.')
    parser.add_argument('path', help='Where to generate the file.')
    parser.set_defaults(_execute=execute)


def execute(args):
    vc = GenerateConfig(args.path)
    vc.execute()
    if len(vc.errors) > 0:
        print('Errors found in: {0}'.format(vc.path))
        for error in vc.errors:
            print(error)
        sys.exit(ExitCodes.FAIL)
    else:
        print('Configuration file written to: {0}'.format(vc.path))
        sys.exit(ExitCodes.SUCCESS)
