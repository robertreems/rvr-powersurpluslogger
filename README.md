# RVR power surplus logger

Average dutch households consume about 30% of the power it produces with solar panels. My goal is to raise that percentage so I'm consuming the power that's been produced by my own house.
I'd like to use it for my home's climate controll and charging the car for example.

This script logs the power surplus, the power I deliver to the enery grid. The logging goes to my Azure log analytics workspace and it sends browsernotifications. These notifications are to inform me when to turn house hold appliances on or off to consume the produced Power myself.
For example when I'll have to start or stop the airco / car charging.

My ultimate goal is to automate all this. But hey you should set some goals.

The power surpluss is measured using a [Home Wizard P1 wifi dongle](https://www.homewizard.nl/shop/homewizard-wi-fi-p1-meter). 

## Prerequistes
[The rvr-base module](https://github.com/robertreems/rvrbase)

This script is developed for Linux and tested on:
- Ubuntu 20.04 using Python 3.8.10.
- An Azure log analytics workspace.
- Raspberry Pi OS using Python 3.9.2.
- a smart energy meter in your home that's compatible with:
- a Home wizard P1 meter.

## Using this script
It reads a configuration file. You'll have to create that first in /etc/rvr/config.ini. Make sure it has the following contents:
```
[AZ GENERAL]
tenant = 83ebf573-f6a0-4a5a-a14e-323ba97ec356

[AZ_LOG_ANALYTICS_WORKSPACE]
workspace_id = 'log analytics workspace_id'
primary_key = 'log analytics primary key'
powerstatistics_workspace_id = 'log analytics workspace_id'
powerstatistics_primary_key = 'log analytics primary key'

[AZ SERVICE PRINCIPAL LOGANALYTICSREADER]
service_principal_loganalyticsreader_id = 'service principal'
service_principal_loganalyticsreader_secret = 'secret'

[HOME_WIZARD_P1]
hwip = IP
```

Then you're able to run the main.py script file.

## Disclaimer
This script has been written for my personal use. Feel free to use it but at your own discression. There is no support or whatsoever on my part. 
