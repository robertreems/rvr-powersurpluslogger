import logging
from rvrbase import Rvrbase

import constants

logging.getLogger().setLevel(logging.INFO)

base = Rvrbase(constants.CONFIG_FILE)

def get_meters_start_day(row):
    # consumption_tariff1 = base.azlog_analyticsq("power_usage_CL | where TimeGenerated > startofday(now()) and  metric_name_s == 'consumption_tariff1' | sort by TimeGenerated asc | limit 1")
    # consumption_tariff2 = base.azlog_analyticsq("power_usage_CL | where TimeGenerated > startofday(now()) and  metric_name_s == 'consumption_tariff2' | sort by TimeGenerated asc | limit 1")
    # delivery_tariff1 = base.azlog_analyticsq("power_usage_CL | where TimeGenerated > startofday(now()) and  metric_name_s == 'delivery_tariff1' | sort by TimeGenerated asc | limit 1")
    # delivery_tariff2 = base.azlog_analyticsq("power_usage_CL | where TimeGenerated > startofday(now()) and  metric_name_s == 'delivery_tariff2' | sort by TimeGenerated asc | limit 1")

    result = base.azlog_analyticsq(f"power_usage_CL | where TimeGenerated > startofday(now()) and  metric_name_s == '{row}' | sort by TimeGenerated asc | limit 1")
    # consumption_tariff1['tables'][0]['rows'][0][11]
    return result['tables'][0]['rows'][0][11]


print(get_meters_start_day('consumption_tariff1'))
print(get_meters_start_day('consumption_tariff2'))
print(get_meters_start_day('delivery_tariff1'))
print(get_meters_start_day('delivery_tariff2'))
    