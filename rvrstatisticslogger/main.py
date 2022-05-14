#!/usr/bin/env python3

import logging
from rvrbase import Rvrbase
from datetime import datetime, date, timedelta

import constants
import cli


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


def calculate_meter_total(meter, start_date, end_date):
    start_daily_measure = get_power_meter(meter, start_date, 'asc')
    end_daily_measure = get_power_meter(meter, end_date, 'desc')

    return round((end_daily_measure - start_daily_measure), 3)


# Get all meter daily totals.
def statistics(start_date, end_date):
    consumption_tariff1 = calculate_meter_total(
        'consumption_tariff1', start_date, end_date)
    consumption_tariff2 = calculate_meter_total(
        'consumption_tariff2', start_date, end_date)
    delivery_tariff1 = calculate_meter_total(
        'delivery_tariff1', start_date, end_date)
    delivery_tariff2 = calculate_meter_total(
        'delivery_tariff2', start_date, end_date)

    # The daily power consumption / production combined.
    day_total_consumption = consumption_tariff1 + consumption_tariff2
    day_total_delivery = delivery_tariff1 + delivery_tariff2
    daily_total = round((day_total_delivery - day_total_consumption), 3)

    # I want to log these values to Azure daily.
    print(f'Daily total: {daily_total}')
    print(
        f'Daily total tariff 1: {delivery_tariff1 - consumption_tariff1}')
    print(
        f'Daily total tariff 2: {delivery_tariff2 - consumption_tariff2}')
    print(consumption_tariff1)
    print(consumption_tariff2)
    print(delivery_tariff1)
    print(delivery_tariff2)

    # base.send_az_metric('power_usage', 'consumption_tariff1', start_c_t1)
    # print(calculate_meter_total('delivery_tariff2', datetime.datetime(2022, 5, 3)))


cli = cli.Cli()
logging.getLogger().setLevel(cli.args.loglevel)

base = Rvrbase(constants.CONFIG_FILE)
start_date = cli.args.startdate.split('-')
year = int(start_date[0])
month = int(start_date[1])
day = int(start_date[2])
start_date = date(year, month, day)
end_date = date.today()

if cli.args.week:
    pass
elif cli.args.month:
    pass
else:
    delta = timedelta(days=1)
    while start_date <= end_date:
        print(start_date.strftime("%Y-%m-%d"))
        start_day = datetime.combine(start_date, datetime.min.time())
        end_day = datetime.combine(start_date, datetime.min.time())

        statistics(start_day, end_day)

        start_date += delta
