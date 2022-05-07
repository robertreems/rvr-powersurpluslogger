import logging
from rvrbase import Rvrbase
import datetime

import constants

logging.getLogger().setLevel(logging.INFO)

base = Rvrbase(constants.CONFIG_FILE)


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



print(get_power_meter('delivery_tariff2', datetime.datetime(2022, 5, 3), 'asc'))
print(get_power_meter('delivery_tariff2', datetime.datetime(2022, 5, 3), 'desc'))
