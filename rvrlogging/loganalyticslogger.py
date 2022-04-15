#!/usr/bin/python3
# from https://medium.com/slalom-build/reading-and-writing-to-azure-log-analytics-c78461056862

import requests
import hashlib
import hmac
import base64
import logging
import json
import datetime
from time import sleep as sleep
import config as config
from constants import CONFIG_FILE


conf = config.config(CONFIG_FILE)

def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
    """Returns authorization header which will be used when sending data into Azure Log Analytics"""
    
    x_headers = 'x-ms-date:' + date
    string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
    bytes_to_hash = bytes(string_to_hash, 'UTF-8')
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode('utf-8')
    authorization = "SharedKey {}:{}".format(customer_id,encoded_hash)
    return authorization

def post_data(customer_id, shared_key, body, log_type):
    """Sends payload to Azure Log Analytics Workspace
    
    Keyword arguments:
    customer_id -- Workspace ID obtained from Advanced Settings
    shared_key -- Authorization header, created using build_signature
    body -- payload to send to Azure Log Analytics
    log_type -- Azure Log Analytics table name
    """
    
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)

    uri = 'https://' + customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }

    response = requests.post(uri,data=body, headers=headers)
    if (response.status_code >= 200 and response.status_code <= 299):
        logging.info('Accepted payload:' + body)
    else:
        logging.error("Unable to Write: " + format(response.status_code))


azure_log_customer_id = conf.q1('workspace_id')
azure_log_shared_key =  conf.q1('primary_key')

url = 'http://nu.nl'
demo_request = requests.get(url)
table_name = 'demoURLMonitor'
data = {
    "status" : demo_request.ok,
    "url" : url,
    "rt_avg" : demo_request.elapsed.total_seconds(),
    "response_code" : demo_request.status_code
}
data_json = json.dumps(data)

try:
    while True:
        post_data(azure_log_customer_id, azure_log_shared_key, data_json, table_name)
        print('posting data')
        sleep(5)

except Exception as error:
    logging.error("Unable to send data to Azure Log")
    logging.error(error)