# -*- coding: utf-8 -*-
"""Use case 1: request asset details - plant data

This code demonstrates how to get the information of every plant in the organization

Example:
    $ python get_plant_data.py

"""

from smart_sensor_client.smart_sensor_client import SmartSensorClient
from pprint import pprint
import argparse

DEFAULT_SETTINGS_FILE = 'settings.yaml'


def run_task(settings_file=DEFAULT_SETTINGS_FILE, debug: bool = False) -> bool:

    # Create the client instance
    client = SmartSensorClient(settings_file=settings_file, debug=debug)

    # Authenticate
    if not client.authenticate():
        print('Authentication FAILED')
        return False

    # Print organization
    print('Organization {}, {}'.format(client.organization_id, client.organization_name))
    print()

    # Get list of plants
    plants = client.get_plant_list()

    # Iterate the plant list and print all assets therein
    for plant in plants:
        pprint(plant)
        print()

    return True


# Main body
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the information of every plant in the organization')
    parser.add_argument('-d', '--debug', action='store_true', help='print debug information such as the sent curl request')
    args = parser.parse_args()

    result = run_task(debug=args.debug)

    if result is True:
        print('Task SUCCESS')
    else:
        print('Task FAILED')
