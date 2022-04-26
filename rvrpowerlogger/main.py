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
    # Get the telegram.
    result = requests.get(f'http://{ip}/api/v1/telegram')

    if result.status_code != 200:
        raise exceptions.HomeWizzardCommunication(
            constants.ERR_UNEXPECTED_HTTP_RESPONSE.format(response=result))

    json_result = result.content.splitlines()

    # Get the specific tarifs in byte string. Select substring 10:19 convert to string and
    # to float. The 5th and 6th line of the telegram message is the Meter Reading
    # electricity delivered by client in 0,001 kWh.
    consumption_tariff1 = float(json_result[3][10:19].decode('utf-8'))
    consumption_tariff2 = float(json_result[4][10:19].decode('utf-8'))
    delivery_tariff1 = float(json_result[5][10:19].decode('utf-8'))
    delivery_tariff2 = float(json_result[6][10:19].decode('utf-8'))

    return consumption_tariff1, consumption_tariff2, delivery_tariff1, delivery_tariff2


def send_notification(active_power_history):
    global is_no_power_notification_send

    if sum(active_power_history) <= 0 and is_no_power_notification_send is False:
        thelogger.log_application_event(
            type='info', message='No power surplus for a prolonged time.',
            notify_message=True)
        is_no_power_notification_send = True

        # Reset is_no_power_notification_send to false in order to send message if there is no
        # longer any surplus.
    elif Average(active_power_history) > 250 and is_no_power_notification_send is True:
        thelogger.log_application_event(
            type='info', message='You have got some juice. Use it!', notify_message=True)
        is_no_power_notification_send = False


# Calculate the power used / produced in 60 seconds and convert it from kWh to Wh.
def calc_power(start_power, end_power):
    current = round(end_power - start_power, 3)
    return((current * 60) * 1000)


def aggregated_power(start_c_t1, start_c_t2, start_d_t1, start_d_t2, end_c_t1, end_c_t2, end_d_t1,
                     end_d_t2):
    consumption_tariff1 = calc_power(start_c_t1, end_c_t1)
    consumption_tariff2 = calc_power(start_c_t2, end_c_t2)
    delivery_tariff1 = calc_power(start_d_t1, end_d_t1)
    delivery_tariff2 = calc_power(start_d_t2, end_d_t2)

    return (delivery_tariff1 + delivery_tariff2) - (consumption_tariff1 + consumption_tariff2)


def run():
    active_power_history = list()

    while True:
        try:
            # c_t1 is consumption tariff 1.
            # d_t1 is delivery tariff 1.
            start_c_t1, start_c_t2, start_d_t1, start_d_t2 = read_meters()

            # Log the current meter values.
            thelogger.post_metric('power_usage', 'consumption_tariff1', start_c_t1)
            thelogger.post_metric('power_usage', 'consumption_tariff2', start_c_t2)
            thelogger.post_metric('power_usage', 'delivery_tariff1', start_d_t1)
            thelogger.post_metric('power_usage', 'delivery_tariff2', start_d_t2)

            sleep(60)

            end_c_t1, end_c_t2, end_d_t1, end_d_t2 = read_meters()

            # Log the current power measurement.
            _aggregated_power = aggregated_power(start_c_t1, start_c_t2, start_d_t1, start_d_t2,
                                                 end_c_t1, end_c_t2, end_d_t1, end_d_t2)
            
            thelogger.post_metric('power_usage', 'aggregated_power', _aggregated_power)

            # Keep a history of max. 10 measurements.
            active_power_history.insert(0, _aggregated_power)
            del active_power_history[10:]

            send_notification(active_power_history)

        except exceptions.HomeWizzardCommunication as error:
            # Todo enable notify_message when method has been implented to prevent an overload of
            # messages.
            thelogger.log_application_event(
                type='error', message=error, notify_message=False)
            sleep(60)

        except Exception as error:
            thelogger.log_application_event(type='error',
                                            message=constants.ERR_UNKNOWN_ERROR.format(
                                                message=error), notify_message=False)
            # Todo enable notify_message when method has
            # been implented to prevent an overload of messages.
            sleep(60)


# Make this scripts functions importable.
if __name__ == '__main__':
    run()
