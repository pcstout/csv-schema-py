import sys
from .validate_csv import ValidateCsv
from ...core import ExitCodes


def create(subparsers, parents):
    parser = subparsers.add_parser('validate-csv',
                                   parents=parents,
                                   help='Validates a CSV file against a schema.')
    parser.add_argument('csv', help='The CSV file to validate.')
    parser.add_argument('schema', help='The schema JSON file.')
    parser.set_defaults(_execute=execute)


def execute(args):
    vc = ValidateCsv(args.csv, args.schema)
    vc.execute()
    if len(vc.errors) > 0:
        print('Errors found in: {0}'.format(vc.csv_path))
        for error in vc.errors:
            print(error)
        sys.exit(ExitCodes.FAIL)
    else:
        print('No errors found in: {0}'.format(vc.csv_path))
        sys.exit(ExitCodes.SUCCESS)
