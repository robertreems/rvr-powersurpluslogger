#!/usr/bin/env python3
import logging
from time import sleep
import mylogger
import requests
import config
from constants import CONFIG_FILE

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get IP of the dongle
conf = config.config(CONFIG_FILE)

ip = conf.q1('hwip')

thelogger = mylogger.mylogger()

thelogger.log_start()


# The initial plan was to use the '/api/v1/data' api to retrieve my solar power surplus from one of the api properties written in 
# https://homewizard-energy-api.readthedocs.io/endpoints.html.
# Unfortunately my "smart" energymeter is very old and provides telegram messages with very limited information. So the '/api/v1/data' 
# doesnt' contain any usable information. The mobile app doesn't show the current power production as well. So I ended up interpreting
# the telegram messages and calculate the surplus based on the provided telegrams. The telegrams are documented here: 
# https://www.netbeheernederland.nl/_upload/Files/Slimme_meter_15_a727fce1f1.pdf. 

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

    # todo create a nice conversion function that does the calculation
    thelogger.post_metric('power_usage', 'active_power_surplus_t1', int(((end_tariff1 - start_tariff1) * 60) * 1000))
    thelogger.post_metric('power_usage', 'active_power_surplus_t2', int(((end_tariff2 - start_tariff2) * 60) * 1000))
