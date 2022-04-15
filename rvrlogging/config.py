from configparser import ConfigParser
from pathlib import Path
import logging
import errno
import os


class config:

    def __init__(self, path):
        self.path = path

        configfile = Path(path)

        if configfile.exists():
            logging.debug('configfile {} exists'.format(path))
            self.readconfig()
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), path)

    def readconfig(self):
        self.config = ConfigParser()
        self.config.read(self.path)

    # Very small implementation for querying configuration INI files.
    # It simply assumes all keys are unique and returns a key if found.
    def q1(self, key):
        for section in self.config.sections():
            if key in self.config[section].keys():
                return self.config[section][key]
                