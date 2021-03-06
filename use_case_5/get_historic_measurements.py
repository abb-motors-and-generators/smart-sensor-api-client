# -*- coding: utf-8 -*-
"""Use case 5: request historic measurement data of an asset - historic

This code prints out some measurement values for a particular asset

Example:
    $ python get_historic_measurements.py

"""

from smart_sensor_client.smart_sensor_client import SmartSensorClient
import dateutil.parser
import matplotlib.pyplot as plt
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

    # Ask users for their input:
    print('Please enter your query parameters:')
    asset_id = input('Asset ID: ')

    # Print possible measurement types for this asset
    possible_measurement_types = client.get_measurement_types(asset_id=asset_id)
    for x in possible_measurement_types:
        print(str(x['measurementTypeName']) + ' -> ' + str(x['measurementTypeID']))

    measurement_type = input('Measurement type (find possible IDs in list above, separated by commas): ')
    start_date = input('Start date (YYYY-MM-DD): ')
    end_date = input('End date (YYYY-MM-DD): ')

    # Get the measurement data during this time
    measurements = client.get_measurement_value(asset_id=asset_id,
                                                measurement_type=measurement_type,
                                                start_time=start_date,
                                                end_time=end_date)

    # Check if measurement is present and then plot the data in subplots
    fig, axs = plt.subplots(len(measurements))
    for index, measurement in enumerate(measurements):
        if measurement['measurements'][0]['measurementValue'] is not None:
            # get values and timestamps into a list
            values_to_plot = [[dateutil.parser.parse(v['measurementCreated']), float(v['measurementValue'])]
                              for v in measurement['measurements']
                              ]
            # sort values by timestamp
            values_to_plot.sort(key=lambda v: v[0])

            # store a separate timestamp and value list
            measurement_timestamp = [v[0] for v in values_to_plot]
            measurement_values = [v[1] for v in values_to_plot]

            # Add data to the subplots and add a title to each subplot
            if len(measurements) == 1:
                axs.plot(measurement_timestamp, measurement_values)
                axs.set_title(measurement['measurementTypeName'])
            else:
                axs[index].plot(measurement_timestamp, measurement_values)
                axs[index].set_title(measurement['measurementTypeName'])
        else:
            # if no measurements were found for this type, print an error message
            print('No measurements for measurement type ' + str(
                measurement['measurementTypeName']) + ' could be fetched.')
            axs[index].set_title(measurement['measurementTypeName'])

    # Display plot
    plt.show()

    return True


# Main body
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot values of one or more measurement types in a defined date range of a chosen asset.')
    parser.add_argument('-d', '--debug', action='store_true', help='print debug information such as the sent curl request')
    args = parser.parse_args()

    result = run_task(debug=args.debug)

    if result is True:
        print('Task SUCCESS')
    else:
        print('Task FAILED')
