#!/usr/bin/env python3

# The initial plan was to use the '/api/v1/data' api to retrieve my solar power surplus from one
# of the api properties written in https://homewizard-energy-api.readthedocs.io/endpoints.html.
# Unfortunately my "smart" energymeter provides telegram messages with very limited information.
# So the '/api/v1/data' doesnt' contain any usable information. The mobile app doesn't show the
# current power production as well. So I ended up interpreting the telegram messages and calculate
# the surplus based on the provided telegrams. The telegrams are documented here:
# https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf.

from time import sleep
import requests
from rvrbase import rvrlogger
from rvrbase import rvrconfig
import constants
import logging
import exceptions


logging.getLogger().setLevel(logging.INFO)

# Get IP of the dongle
conf = rvrconfig.Rvrconfig(constants.CONFIG_FILE)
ip = conf.q1('hwip')
thelogger = rvrlogger.Rvrlogger()
is_no_power_notification_send = False


def Average(lst):
    return sum(lst) / len(lst)

def read_meters():
    # Get the telegram
    result = requests.get(f'http://{ip}/api/v1/telegram')

    if result.status_code != 200:
        raise exceptions.HomeWizzardCommunication(
            constants.ERR_UNEXPECTED_HTTP_RESPONSE.format(response=result))

    json_result = result.content.splitlines()

    # Get the specific tarifs in byte string. Select substring 10:19 convert to string and
    # to float. The 5th and 6th line of the telegram message is the Meter Reading
    # electricity delivered by client in 0,001 kWh.
    tariff1 = float(json_result[5][10:19].decode('utf-8'))
    tariff2 = float(json_result[6][10:19].decode('utf-8'))

    return tariff1, tariff2

def read_meters_enery_delivered():
    # Get the telegram
    result = requests.get(f'http://{ip}/api/v1/telegram')

    if result.status_code != 200:
        raise exceptions.HomeWizzardCommunication(
            constants.ERR_UNEXPECTED_HTTP_RESPONSE.format(response=result))

    json_result = result.content.splitlines()

    # Get the specific tarifs in byte string. Select substring 10:19 convert to string and
    # to float. The 5th and 6th line of the telegram message is the Meter Reading
    # electricity delivered by client in 0,001 kWh.
    tariff1 = float(json_result[5][10:19].decode('utf-8'))
    tariff2 = float(json_result[6][10:19].decode('utf-8'))

    return tariff1, tariff2


def send_notification(active_power_history):
    global is_no_power_notification_send

    if sum(active_power_history) == 0 and is_no_power_notification_send is False:
        thelogger.log_application_event(
            type='info', message='No power surplus for a prolonged time.',
            notify_message=True)
        is_no_power_notification_send = True

        # Reset is_no_power_notification_send to false in order to send message if there is no
        # longer any surplus.
    elif Average(active_power_history) > 250 and is_no_power_notification_send is True:
        thelogger.log_application_event(
            type='info', message=f'You have got some juice. An average of \
                        {Average(active_power_history)} surplus in the past 10 minutes. Use it!',
            notify_message=True)
        is_no_power_notification_send = False


def run():
    active_power_history = list()

    while True:
        try:
            start_tariff1, start_tariff2 = read_meters_enery_delivered()

            sleep(60)

            end_tariff1, end_tariff2 = read_meters_enery_delivered()

            # Log the current power measurement.
            active_power_tariff1 = int(
                ((end_tariff1 - start_tariff1) * 60) * 1000)
            active_power_tariff2 = int(
                ((end_tariff2 - start_tariff2) * 60) * 1000)
            thelogger.post_metric(
                'power_usage', 'active_power_surplus_t1', active_power_tariff1)
            thelogger.post_metric(
                'power_usage', 'active_power_surplus_t2', active_power_tariff2)

            # Keep a history of max. 20 measurements.
            active_power_history.insert(0, active_power_tariff1)
            active_power_history.insert(0, active_power_tariff2)
            del active_power_history[20:]

            send_notification(active_power_history)

        except exceptions.HomeWizzardCommunication as error:
            # todo enalble notify_message when method has been implented to prevent an overload of
            # messages.
            thelogger.log_application_event(
                type='error', message=error, notify_message=False)
            sleep(60)

        except Exception as error:
            thelogger.log_application_event(type='error',
                                            message=constants.ERR_UNKNOWN_ERROR.format(
                                                message=error), notify_message=False)
            # todo enalble notify_message when method has
            # been implented to prevent an overload of messages.
            sleep(60)


# Make this scripts functions importable.
if __name__ == '__main__':
    run()
