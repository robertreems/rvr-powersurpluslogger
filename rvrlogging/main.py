#!/usr/bin/env python3
import logging
import loganalyticslogger
from time import sleep as sleep

try:
    # loganalyticslogger.post_application_event(type='info', message='testing123')
    loganalyticslogger.post_application_starting_event()

except Exception as error:
    logging.error("Unable to send data to Azure Log")
    logging.error(error)
