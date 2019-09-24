# -*- coding: utf-8 -*-
"""Example 3

This code demonstrates how to get the asset details of all assets belonging to the user's organization.

Example:
    $ python example_3_detailed_asset_data.py

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
        print('Plant {}, {}:'.format(plant['plantID'], plant['plantName']))
        print('Assets:')

        # Get list of assets
        assets = client.get_asset_list(organization_id=client.organization_id, plant_id=plant['plantID'])
        if len(assets) == 0:
            print('No assets in this plant')
        else:
            for asset in assets:
                asset_data = client.asset_get_asset_by_id(asset_id=asset['assetID'])
                print('Detailed data of Asset {}, {}:'.format(asset['assetID'], asset['assetName']))
                pprint(asset_data)
                print()

        print()

    return True


# Main body
if __name__ == '__main__':

    result = run_task()

    if result is True:
        print('Task SUCCESS')
    else:
        print('Task FAILED')
