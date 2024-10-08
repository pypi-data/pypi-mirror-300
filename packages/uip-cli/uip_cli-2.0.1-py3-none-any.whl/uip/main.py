from colorama import init, deinit, Fore
from uip.cliconfig.setupcli import setup_cli_args
from uip.config import config
from uip.utils import formatting
from uip.constants import constants
import sys


def main(args_list=sys.argv[1:]):
    """
    Entry point of the CLI
    """

    exit_code = constants.SUCCESS

    try:
        init()

        config.create_global_config_file()
        setup_cli_args(args_list)
    except Exception as e:
        message = formatting.format_error_style(e)
        print(Fore.RED + message, file=sys.stderr)
        exit_code = constants.ERROR
    finally:
        deinit()

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
