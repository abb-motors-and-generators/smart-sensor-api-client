# -*- coding: utf-8 -*-
"""Use case 2: receive notifications for maintenance alerts and alarms

This code demonstrates how to sign up a webhook or another notification channel, which connects an external URL with the smartsensor platform.

Example:
    $ python add_notification_channel.py -a >ASSET ID LIST< -t >NOTIFICATION TYPE< -c >NOTIFICATION CHANNEL< -u >URL<

"""

from smart_sensor_client.smart_sensor_client import SmartSensorClient
import argparse

DEFAULT_SETTINGS_FILE = 'settings.yaml'


def run_task(settings_file=DEFAULT_SETTINGS_FILE, asset_list=None, notification_type=None, notification_channel=None, url=None, debug: bool = False) -> bool:
    # Create the client instance
    client = SmartSensorClient(settings_file=settings_file, debug=debug)

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
    parser.add_argument('-a', '--asset-list', nargs='+',  help='possibly multiple asset IDs for which the notification should be setup', type=int, required=True)
    parser.add_argument('-t', '--notification-type', type=int, help='an integer for the notification type')
    parser.add_argument('-c', '--notification-channel', type=int, help='an integer for the notification channel')
    parser.add_argument('-u', '--url', type=str, help='an url where the webhook should be attached to')
    parser.add_argument('-d', '--debug', action='store_true', help='print debug information such as the sent curl request')
    args = parser.parse_args()

    result = run_task(asset_list=args.asset_list, notification_type=args.notification_type, notification_channel=args.notification_channel, url=args.url, debug=args.debug)

    if result is True:
        print('Task SUCCESS')
    else:
        print('Task FAILED')
