#!/usr/bin/env python

import sys
import json
import requests
from requests.auth import HTTPBasicAuth

CHAT_ID = "xxxxxxxxx"

try:
    # Read configuration parameters
    alert_file = open(sys.argv[1])
    hook_url = sys.argv[3]

    log_msg = "Reading configuration parameters..."
    requests.post(hook_url, headers={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}, data=json.dumps({
        'chat_id': CHAT_ID,
        'text': log_msg
    }))

    # Read the alert file
    log_msg = "Reading the alert file..."
    requests.post(hook_url, headers={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}, data=json.dumps({
        'chat_id': CHAT_ID,
        'text': log_msg
    }))
    alert_json = json.loads(alert_file.read())
    alert_file.close()

    # Extract data fields
    log_msg = "Extracting data fields..."
    requests.post(hook_url, headers={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}, data=json.dumps({
        'chat_id': CHAT_ID,
        'text': log_msg
    }))
    alert_level = alert_json['rule']['level'] if 'rule' in alert_json and 'level' in alert_json['rule'] else "N/A"
    description = alert_json['rule']['description'] if 'rule' in alert_json and 'description' in alert_json['rule'] else "N/A"
    agent = alert_json['agent']['name'] if 'agent' in alert_json and 'name' in alert_json['agent'] else "N/A"
    rule_id = alert_json['rule']['id'] if 'rule' in alert_json and 'id' in alert_json['rule'] else None

    # Debug: send debug info to Telegram
    debug_msg = f"Rule ID: {rule_id} (type: {type(rule_id)})"
    requests.post(hook_url, headers={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}, data=json.dumps({
        'chat_id': CHAT_ID,
        'text': debug_msg
    }))

    # Only proceed if the rule_id is 100303 or 510
    if str(rule_id) in ["100303", "510"]:
        log_msg = f"Rule ID matches {rule_id}. Proceeding with alert..."
        requests.post(hook_url, headers={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}, data=json.dumps({
            'chat_id': CHAT_ID,
            'text': log_msg
        }))
        # Generate request
        msg_data = {}
        msg_data['chat_id'] = CHAT_ID
        msg_data['text'] = f"Description: {description}\nAlert Level: {alert_level}\nAgent: {agent}\nRule ID: {rule_id}"
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

        # Send the request
        log_msg = "Sending alert to Telegram..."
        requests.post(hook_url, headers={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}, data=json.dumps({
            'chat_id': CHAT_ID,
            'text': log_msg
        }))
        response = requests.post(hook_url, headers=headers, data=json.dumps(msg_data))

        # Send response status for debugging
        response_msg = f"Response status code: {response.status_code}"
        if response.status_code != 200:
            response_msg += f"\nError: {response.text}"

        requests.post(hook_url, headers={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}, data=json.dumps({
            'chat_id': CHAT_ID,
            'text': response_msg
        }))

    else:
        skip_msg = f"Rule ID does not match 100303 or 510. Skipping alert. Rule ID: {rule_id}"
        requests.post(hook_url, headers={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}, data=json.dumps({
            'chat_id': CHAT_ID,
            'text': skip_msg
        }))

except Exception as e:
    error_msg = f"An error occurred: {str(e)}"
    requests.post(hook_url, headers={'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}, data=json.dumps({
        'chat_id': CHAT_ID,
        'text': error_msg
    }))

sys.exit(0)
