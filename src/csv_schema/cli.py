import sys
import argparse
from .core import ExitCodes
from .commands.validate_config import cli as validate_config_cli
from .commands.validate_csv import cli as validate_csv_cli
from .commands.generate_config import cli as generate_config_cli
from ._version import __version__

ALL_ACTIONS = [validate_config_cli, validate_csv_cli, generate_config_cli]


def main(args=None):
    shared_parser = argparse.ArgumentParser(add_help=False)

    main_parser = argparse.ArgumentParser(description='CSV Schema')
    main_parser.add_argument('--version', action='version',version='%(prog)s {0}'.format(__version__))

    subparsers = main_parser.add_subparsers(title='Commands', dest='command')
    for action in ALL_ACTIONS:
        action.create(subparsers, [shared_parser])

    cmd_args = main_parser.parse_args(args)

    if '_execute' in cmd_args:
        cmd_args._execute(cmd_args)
    else:
        main_parser.print_help()
        sys.exit(ExitCodes.FAIL)
