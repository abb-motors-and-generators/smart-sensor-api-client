# -*- coding: utf-8 -*-
"""Example 2

This code demonstrates how to get the information of every plant in the organization

Example:
    $ python use_case_2_plant_data.py

"""

from smart_sensor_client.smart_sensor_client import SmartSensorClient
from pprint import pprint

DEFAULT_SETTINGS_FILE = 'settings.yaml'


def run_task(settings_file=DEFAULT_SETTINGS_FILE) -> bool:

    # Create the client instance
    client = SmartSensorClient(settings_file=settings_file)

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

    result = run_task()

    if result is True:
        print('Task SUCCESS')
    else:
        print('Task FAILED')
