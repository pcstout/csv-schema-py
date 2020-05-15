from .validate_config import ValidateConfig


def create(subparsers, parents):
    parser = subparsers.add_parser('validate-config',
                                   parents=parents,
                                   help='Validates the CSV schema JSON configuration file.')
    parser.add_argument('schema', help='The JSON file to validate.')
    parser.set_defaults(_execute=execute)


def execute(args):
    ValidateConfig(args.schema).execute()
