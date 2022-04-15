#!/usr/bin/python3
# from https://medium.com/slalom-build/reading-and-writing-to-azure-log-analytics-c78461056862

import json
import sys
import requests
import hashlib
import hmac
import base64
import logging
import datetime
from platform import node
import config as config
from constants import CONFIG_FILE, LOG_TYPE_APPLICATION_EVENT


class Log_analytics_logger:

    def __init__(self):
        self.conf = config.config(CONFIG_FILE)

    def build_signature(self, customer_id, shared_key, date, content_length, method, content_type, resource):
        """Returns authorization header which will be used when sending data into Azure Log Analytics"""

        x_headers = 'x-ms-date:' + date
        string_to_hash = method + "\n" + \
            str(content_length) + "\n" + content_type + \
            "\n" + x_headers + "\n" + resource
        bytes_to_hash = bytes(string_to_hash, 'UTF-8')
        decoded_key = base64.b64decode(shared_key)
        encoded_hash = base64.b64encode(hmac.new(
            decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode('utf-8')
        authorization = "SharedKey {}:{}".format(customer_id, encoded_hash)
        return authorization


    def post_data(self, body, log_type):
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
        signature = self.build_signature(
            self.conf.q1('workspace_id'), self.conf.q1('primary_key'), rfc1123date, content_length, method, content_type, resource)

        uri = 'https://' + self.conf.q1('workspace_id') + '.ods.opinsights.azure.com' + \
            resource + '?api-version=2016-04-01'

        headers = {
            'content-type': content_type,
            'Authorization': signature,
            'Log-Type': log_type,
            'x-ms-date': rfc1123date
        }

        response = requests.post(uri, data=body, headers=headers)
        if (response.status_code >= 200 and response.status_code <= 299):
            logging.info('Accepted payload:' + body)
        else:
            logging.error("Unable to Write: " + format(response.status_code)) # todo throw


    def post_application_event(self, type, message): # todo use enum for type
        body = {
            "hostname": node(),
            "script_path": sys.argv[0],
            "arguments" : sys.argv[1:],
            "type": type,
            "message": message
        }

        body_json = json.dumps(body)

        self.post_data(body_json, LOG_TYPE_APPLICATION_EVENT)

    def post_application_starting_event(self):
        self.post_application_event('info', 'Starting')