"""
    This class handles the CLI opions and arguments.
"""

from argparse import ArgumentParser
from datetime import datetime


class Cli:
    args = ''

    def __init__(self):
        description = "Calculates and exports powerconsumption and usage statistics over a given\
            period."

        parser = ArgumentParser(description=description)

        parser.add_argument(
            "-s", "--startdate",
            help='defines the startdate in format YYYY-MM-DD',
            type=str,
            default=datetime.now().strftime("%Y-%m-%d")
        )
        parser.add_argument(
            "-w", "--week",
            help='report statistics for one or more weeks, if no startdate provided only the\
                current week will be exported.',
            action='store_true'
        )
        parser.add_argument(
            "-m", "--month",
            help='report statistics for one or more weeks, if no startdate provided only the\
                current month will be exported.',
            action='store_true'
        )
        parser.add_argument(
            "--log_to_azure",
            help='Sends the statistics to Azure.',
            action='store_true'
        )
        parser.add_argument(
            "-l", "--loglevel",
            help='sets the loglevel (CRITICAL = 50 ERROR = 40 WARNING = 30 INFO = 20 DEBUG = 10\
                NOTSET = 0)',
            type=int,
            default=30
        )

        self.args = parser.parse_args()
