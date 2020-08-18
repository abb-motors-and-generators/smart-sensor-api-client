# -*- coding: utf-8 -*-
"""Use case 4: request condition indexes of an asset

This code demonstrates how to get the condition indexes of one or multiple assets.

Example:
    $ python get_condition_indexes.py -a <ASSET ID LIST>

"""

from smart_sensor_client.smart_sensor_client import SmartSensorClient
from pprint import pprint
import argparse

DEFAULT_SETTINGS_FILE = 'settings.yaml'


def run_task(settings_file=DEFAULT_SETTINGS_FILE, asset_list=None, debug: bool = False) -> bool:
    # Create the client instance
    client = SmartSensorClient(settings_file=settings_file, debug=debug)

    # Authenticate
    if not client.authenticate():
        print('Authentication FAILED')
        return False

    if asset_list is None:
        return False

    # Add a notification channel
    response = client.get_condition_index(asset_list)

    # parse response and print the condition indexes for each asset
    for asset in response:
        print('\nAsset ID: ' + str(asset['assetID']))
        for entry in asset['condition']:
            string_to_print = str(entry['conditionIndexName']) + ': ' + str(entry['conditionIndexStatus']['status'])

            # add the status code message to the print if it contains informations
            if entry['conditionIndexStatus']['statusCodeMessage'] is not None:
                string_to_print += ' (' + str(entry['conditionIndexStatus']['statusCodeMessage']) + ')'

            print(string_to_print)

    if response is False:
        return False

    return True


# Main body
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the condition indexes of one or multiple assets.')
    parser.add_argument('-a', '--asset-list', nargs='+',  help='possibly multiple asset IDs for which the notification should be setup', type=int, required=True)
    parser.add_argument('-d', '--debug', action='store_true', help='print debug information such as the sent curl request')
    args = parser.parse_args()

    result = run_task(debug=args.debug, asset_list=args.asset_list)

    if result is True:
        print('Task SUCCESS')
    else:
        print('Task FAILED')
