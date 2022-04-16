from dbus import ValidationException
import loganalyticslogger
import logging
from platform import node
from constants import NOTIFY_APPLICATION_EVENT, VALID_MESSAGE_TYPES
from notify_run import Notify


# Todo maak netjes
class mylogger(loganalyticslogger.Log_analytics_logger):

    def __init__(self):
        super().__init__()
        self.notify = Notify()

        if not self.notify.config_file_exists:
            self.notify.register()

        self.__log_start()

    def __log_start(self):
        message = f'Starting, notify URL: {self.notify.endpoint}'
        self.log_application_event(type='info', message=message)

    def log_application_event(self, type, message, notify_message=False):
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

        if notify_message:
            self.notify.send(NOTIFY_APPLICATION_EVENT.format(type=type, node=node(), message=message))
