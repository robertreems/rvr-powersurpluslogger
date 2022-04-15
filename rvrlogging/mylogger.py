from dbus import ValidationException
import loganalyticslogger
import logging

from constants import VALID_MESSAGE_TYPES


class mylogger(loganalyticslogger.Log_analytics_logger):

    def __init__(self):
        super().__init__()

    def log_start(self):
        self.post_application_starting_event()
        logging.info('starting')

    def log_application_event(self, type, message):
        if not type in VALID_MESSAGE_TYPES:
            raise ValidationException(
                f'{type} is not in {VALID_MESSAGE_TYPES}.')

        self.post_application_event(type, message)

        if type == 'debug':
            logging.debug(message)
        elif type == 'info':
            logging.info(message)
        elif type == 'warning':
            logging.warning(message)
        elif type == 'error':
            logging.error(message)
