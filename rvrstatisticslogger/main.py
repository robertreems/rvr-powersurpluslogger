#!/usr/bin/env python3

import logging
from posixpath import split
from rvrbase import Rvrbase
from datetime import datetime, date, timedelta

import constants
import cli


logging.getLogger().setLevel(logging.INFO)

base = Rvrbase(constants.CONFIG_FILE)

cli = cli.Cli()

start_date = cli.args.startdate.split('-')
year = int(start_date[0])
month = int(start_date[1])
day = int(start_date[2])

# start_date = date(year, month, day)
# end_date = date(2022, 5, 13)
# delta = timedelta(days=1)
# while start_date <= end_date:
#     print(start_date.strftime("%Y-%m-%d"))
#     start_date += delta
    

# day_to_monitor = datetime(year, month, day)


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
def day_meter(day_to_monitor):
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


start_date = date(year, month, day)
end_date = date.today()
delta = timedelta(days=1)
while start_date <= end_date:
    print(start_date.strftime("%Y-%m-%d"))
    
    day_meter(datetime.combine(start_date, datetime.min.time()))

    start_date += delta