#!/usr/bin/env python3

import logging
from rvrbase import Rvrbase
from datetime import date, timedelta
from calendar import monthrange

import constants
import cli


def get_power_meter(row, date, sort_order):
    day = date.strftime("%Y-%m-%d")

    query = f"power_usage_CL | where TimeGenerated > startofday(datetime({day})) \
        and TimeGenerated < endofday(datetime({day}))\
        and metric_name_s == '{row}'\
        | sort by TimeGenerated {sort_order}\
        | limit 1"

    result = base.azlog_analyticsq(query=query)
    return result['tables'][0]['rows'][0][11]


def calculate_meter_total(meter, start_date, end_date):
    try:
        start_daily_measure = get_power_meter(meter, start_date, 'asc')
    except IndexError:
        start_daily_measure = 0

    try:
        end_daily_measure = get_power_meter(meter, end_date, 'desc')
    except IndexError:
        end_daily_measure = 0

    return round((end_daily_measure - start_daily_measure), 3)


# Get all the meters, and send the calculated statistics to Azure.
def process_statistics(start_date, end_date):
    today = date.today()

    # Prevent looking in the future.
    if today < end_date:
        end_date = today

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
    print(f'Total: {daily_total}')
    print(
        f'Total tariff 1: { round((delivery_tariff1 - consumption_tariff1), 3)}')
    print(
        f'Total tariff 2: {round((delivery_tariff2 - consumption_tariff2), 3)}')
    print(consumption_tariff1)
    print(consumption_tariff2)
    print(delivery_tariff1)
    print(delivery_tariff2)

    # base.send_az_metric('power_usage', 'consumption_tariff1', start_c_t1)


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
    delta = timedelta(weeks=1)
    while start_date <= end_date:
        year = int(start_date.strftime("%Y"))
        week = int(start_date.strftime("%U"))

        monday = date.fromisocalendar(year=year, week=week, day=1)
        sunday = date.fromisocalendar(year=year, week=week, day=7)

        print(f"{monday} - {sunday}")

        process_statistics(start_date=monday, end_date=sunday)

        start_date += delta

elif cli.args.month:
    while start_date <= end_date:
        year = int(start_date.strftime("%Y"))
        month = int(start_date.strftime("%m"))

        first_month_day = start_date.replace(day=1)
        _, days_in_month = monthrange(year=year, month=month)
        last_month_day = start_date.replace(day=days_in_month)

        print(f"{first_month_day} - {last_month_day}")

        process_statistics(start_date=first_month_day, end_date=last_month_day)
        delta = timedelta(days=days_in_month)
        start_date += delta
else:
    delta = timedelta(days=1)
    while start_date <= end_date:
        print(start_date.strftime("%Y-%m-%d"))
        process_statistics(start_date=start_date, end_date=start_date)

        start_date += delta
