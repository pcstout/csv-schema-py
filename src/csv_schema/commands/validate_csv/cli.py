from .validate_csv import ValidateCsv


def create(subparsers, parents):
    parser = subparsers.add_parser('validate-csv',
                                   parents=parents,
                                   help='Validates a CSV file against a schema.')
    parser.add_argument('csv', help='The CSV file to validate.')
    parser.add_argument('schema', help='The schema JSON file.')
    parser.set_defaults(_execute=execute)


def execute(args):
    ValidateCsv(args.csv, args.schema).execute()
