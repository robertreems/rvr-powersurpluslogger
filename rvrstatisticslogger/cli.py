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

        self.args = parser.parse_args()
