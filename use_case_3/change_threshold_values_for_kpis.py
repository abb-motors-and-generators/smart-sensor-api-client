# -*- coding: utf-8 -*-
"""Use Case 3: Change Threshold Values for KPIs

This code demonstrates how to change the KPI threshold values of an asset.

Example:
    $ python use_case_3/change_threshold_values_for_kpis.py -a <ASSET ID > -m <MEASUREMENT TYPE> -v <VALUE LIST>

"""

from smart_sensor_client.smart_sensor_client import SmartSensorClient
import argparse

DEFAULT_SETTINGS_FILE = 'settings.yaml'


def run_task(settings_file=DEFAULT_SETTINGS_FILE, asset_id=None, measurement_type=None, value_list=None,
             debug: bool = False) -> bool:
    # Create the client instance
    client = SmartSensorClient(settings_file=settings_file, debug=debug)

    # Authenticate
    if not client.authenticate():
        print('Authentication FAILED')
        return False

    # Check if all arguments were passed
    if asset_id is None or measurement_type is None or value_list is None:
        return False

    # Change the KPI threshold
    response = client.change_kpi_threshold(asset_id, measurement_type, value_list)

    if response is False:
        return False

    # Print success message
    print('Changed thresholds of asset ' + str(asset_id) + ' for measurement type ' + str(measurement_type) + ' to:')
    print('Healthy: ' + str(value_list[0]) + ' to ' + str(value_list[1]))
    print('Weak: ' + str(value_list[1]) + ' to ' + str(value_list[2]))
    print('Critical: ' + str(value_list[2]) + ' to ' + str(value_list[3]))

    return True


# Main body
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Change the thresholds for warnings and alarms of the KPIs')
    parser.add_argument('-a', '--asset-id', type=int, help='an integer for the asset ID', required=True)
    parser.add_argument('-m', '--measurement-type', type=int, help='an integer for the measurement type', required=True)
    parser.add_argument('-v', '--value-list', nargs='+',
                        help='list of four values which define the thresholds of Healthy, Weak and Critical', type=int,
                        required=True)

    parser.add_argument('-d', '--debug', action='store_true',
                        help='print debug information such as the sent curl request')
    args = parser.parse_args()

    result = run_task(debug=args.debug, asset_id=args.asset_id, measurement_type=args.measurement_type,
                      value_list=args.value_list)

    if result is True:
        print('Task SUCCESS')
    else:
        print('Task FAILED')
