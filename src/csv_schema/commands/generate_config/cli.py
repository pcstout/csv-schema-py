import sys
from .generate_config import GenerateConfig
from ...core import ExitCodes


def create(subparsers, parents):
    parser = subparsers.add_parser('generate-config',
                                   parents=parents,
                                   help='Generate a CSV schema JSON configuration file.')
    parser.add_argument('path', help='Where to generate the file.')
    parser.add_argument('--with-csv',
                        default=False,
                        action='store_true',
                        help='Generate a test CSV file to go along with the schema.')
    parser.add_argument('--with-csv-rows',
                        default=100,
                        type=int,
                        help='How many rows to generate in the CSV file.')
    parser.set_defaults(_execute=execute)


def execute(args):
    vc = GenerateConfig(args.path, with_csv=args.with_csv, with_csv_rows=args.with_csv_rows)
    vc.execute()
    if len(vc.errors) > 0:
        print('Errors found in: {0}'.format(vc.path))
        for error in vc.errors:
            print(error)
        sys.exit(ExitCodes.FAIL)
    else:
        print('Configuration file written to: {0}'.format(vc.path))
        if args.with_csv:
            print('CSV file written to: {0}'.format(vc.csv_path))
        sys.exit(ExitCodes.SUCCESS)
