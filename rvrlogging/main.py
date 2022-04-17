#!/usr/bin/env python3
import logging
from time import sleep
import requests
from rvrbase import rvrlogger
from rvrbase import rvrconfig
from rvrbase import constants

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Get IP of the dongle
conf = rvrconfig.Rvrconfig(constants.CONFIG_FILE)
ip = conf.q1('hwip')
thelogger = rvrlogger.Rvrlogger()
is_no_power_notification_send = False

# The initial plan was to use the '/api/v1/data' api to retrieve my solar power surplus from one of the api properties written in
# https://homewizard-energy-api.readthedocs.io/endpoints.html.
# Unfortunately my "smart" energymeter provides telegram messages with very limited information. So the '/api/v1/data' doesnt' contain
# any usable information. The mobile app doesn't show the current power production as well. So I ended up interpreting the telegram
# messages and calculate the surplus based on the provided telegrams. The telegrams are documented here:
# https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf.


def Average(lst):
    return sum(lst) / len(lst)


active_power_history = list()

while True:
    # Get the telegram
    result = requests.get(f'http://{ip}/api/v1/telegram')
    json_result = result.content.splitlines()

    # Get the specific tarifs in byte string. Select substring 10:19 convert to string and to float.
    # The 5th and 6th line of the telegram message is the Meter Reading electricity delivered by client in 0,001 kWh.
    start_tariff1 = float(json_result[5][10:19].decode('utf-8'))
    start_tariff2 = float(json_result[6][10:19].decode('utf-8'))
    sleep(60)

    result = requests.get(f'http://{ip}/api/v1/telegram')
    json_result = result.content.splitlines()
    end_tariff1 = float(json_result[5][10:19].decode('utf-8'))
    end_tariff2 = float(json_result[6][10:19].decode('utf-8'))

    # Log the current power
    active_power_tariff1 = int(((end_tariff1 - start_tariff1) * 60) * 1000)
    active_power_tariff2 = int(((end_tariff2 - start_tariff2) * 60) * 1000)
    thelogger.post_metric(
        'power_usage', 'active_power_surplus_t1', active_power_tariff1)
    thelogger.post_metric(
        'power_usage', 'active_power_surplus_t2', active_power_tariff2)

    # Send a notification message if there is no energy surplus for a prolonged time.
    active_power_history.insert(0, active_power_tariff1)
    active_power_history.insert(0, active_power_tariff2)

    # remove the measurements after x measures.
    del active_power_history[20:]

    if sum(active_power_history) == 0 and is_no_power_notification_send is False:
        thelogger.log_application_event(
            type='info', message='No power surplus for a prolonged time.', notify_message=True)
        is_no_power_notification_send = True

    # Reset is_no_power_notification_send to false in order to send message if there is no longer any surplus.
    elif Average(active_power_history) > 500 and is_no_power_notification_send is True:
        thelogger.log_application_event(
            type='info', message=f'You have got some juice. {sum(active_power_history)} Watts surplus in the past 10 minutes. Use it!', notify_message=True)
        is_no_power_notification_send = False
