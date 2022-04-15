#!/usr/bin/env python3
import logging
import mylogger

logger = logging.getLogger()
logger.setLevel(logging.INFO)

thelogger = mylogger.mylogger()

thelogger.log_start()

# mylogger = loganalyticslogger.Log_analytics_logger()

# mylogger.post_application_starting_event()

# try:
#     # loganalyticslogger.post_application_event(type='info', message='testing123')
#     # api.loganalyticslogger.post_application_starting_event()

# except Exception as error:
#     logging.error("Unable to send data to Azure Log")
#     logging.error(error)
