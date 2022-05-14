"""
    This class handles the CLI opions and arguments.
"""

from argparse import ArgumentParser
from datetime import datetime


class Cli:
    args = ''

    def __init__(self):
        parser = ArgumentParser()

        parser.add_argument(
            "-s", "--startdate",
            help='Provide the startdate in format YYYY-MM-DD',
            type=str,
            default=datetime.now().strftime("%Y-%m-%d")
        )
        parser.add_argument(
            "-w", "--week",
            help='todo',
            action='store_true'
        )
        parser.add_argument(
            "-m", "--month",
            help='todo',
            action='store_true'
        )
        parser.add_argument(
            "-y", "--year",
            help='todo',
            action='store_true'
        )
        parser.add_argument(
            "-l", "--loglevel",
            help='todo, defaults to warning (CRITICAL = 50 ERROR = 40 WARNING = 30 INFO = 20\
                DEBUG = 10 NOTSET = 0)',
            type=int,
            default=30
        )

        self.args = parser.parse_args()
