# -*- coding: utf-8 -*-
"""Example 6

This code demonstrates how to sign up a webhook or another notification channel, which connects an external URL with the smartsensor platform.

Example:
    $ python use_case_6_add_notification_channel.py >ASSET ID LIST< -nt >NOTIFICATION TYPE< -nc >NOTIFICATION CHANNEL< -u >URL<

"""

from smart_sensor_client.smart_sensor_client import SmartSensorClient
import argparse

DEFAULT_SETTINGS_FILE = 'settings.yaml'


def run_task(settings_file=DEFAULT_SETTINGS_FILE, asset_list=None, notification_type=None, notification_channel=None, url=None) -> bool:
    # Create the client instance
    client = SmartSensorClient(settings_file=settings_file)

    # Authenticate
    if not client.authenticate():
        print('Authentication FAILED')
        return False

    # Add a notification channel
    response = client.add_notification_channel(notification_type, notification_channel, asset_list, url)

    if response is False:
        return False

    return True


# Main body
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add a notification channel to the smart sensor platform.')
    parser.add_argument('asset_list', metavar='asset', type=int, nargs='+', help='possibly multiple asset IDs for which the notification should be setup')
    parser.add_argument('-nt', '--notification_type', type=int, help='an integer for the notification type')
    parser.add_argument('-nc', '--notification_channel', type=int, help='an integer for the notification channel')
    parser.add_argument('-u', '--url', type=str, help='an url where the webhook should be attached to')
    args = parser.parse_args()

    result = run_task(asset_list=args.asset_list, notification_type=args.notification_type, notification_channel=args.notification_channel, url=args.url)

    if result is True:
        print('Task SUCCESS')
    else:
        print('Task FAILED')

