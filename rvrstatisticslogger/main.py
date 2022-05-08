import logging
from rvrbase import Rvrbase
import datetime

import constants

logging.getLogger().setLevel(logging.INFO)

base = Rvrbase(constants.CONFIG_FILE)
day_to_monitor = datetime.datetime(2022, 5, 5)


def get_power_meter(row, date, sort_order):
    # todo validate sort_order.

    day = date.strftime("%Y-%m-%d")

    query = f"power_usage_CL | where TimeGenerated > startofday(datetime({day})) \
        and TimeGenerated < endofday(datetime({day}))\
        and metric_name_s == '{row}'\
        | sort by TimeGenerated {sort_order}\
        | limit 1"

    result = base.azlog_analyticsq(query=query)
    return result['tables'][0]['rows'][0][11]

# print(get_power_meter('delivery_tariff2', datetime.datetime(2022, 5, 3), 'asc'))
# print(get_power_meter('delivery_tariff2', datetime.datetime(2022, 5, 3), 'desc'))


def calculate_meter_daily_total(meter, date):
    start_daily_measure = get_power_meter(meter, date, 'asc')
    end_daily_measure = get_power_meter(meter, date, 'desc')

    return round((end_daily_measure - start_daily_measure), 3)


# Get all meter daily totals.
dt_consumption_tariff1 = calculate_meter_daily_total(
    'consumption_tariff1', day_to_monitor)
dt_consumption_tariff2 = calculate_meter_daily_total(
    'consumption_tariff2', day_to_monitor)
dt_delivery_tariff1 = calculate_meter_daily_total(
    'delivery_tariff1', day_to_monitor)
dt_delivery_tariff2 = calculate_meter_daily_total(
    'delivery_tariff2', day_to_monitor)

# The daily power consumption / production combined.
day_total_consumption = dt_consumption_tariff1 + dt_consumption_tariff2
day_total_delivery = dt_delivery_tariff1 + dt_delivery_tariff2
daily_total = round((day_total_delivery - day_total_consumption), 3)

# I want to log these values to Azure daily.
print(f'Daily total: {daily_total}')
print(f'Daily total tariff 1: {dt_delivery_tariff1 - dt_consumption_tariff1}')
print(f'Daily total tariff 2: {dt_delivery_tariff2 - dt_consumption_tariff2}')
print(dt_consumption_tariff1)
print(dt_consumption_tariff2)
print(dt_delivery_tariff1)
print(dt_delivery_tariff2)

# base.send_az_metric('power_usage', 'consumption_tariff1', start_c_t1)
# print(calculate_meter_daily_total('delivery_tariff2', datetime.datetime(2022, 5, 3)))
