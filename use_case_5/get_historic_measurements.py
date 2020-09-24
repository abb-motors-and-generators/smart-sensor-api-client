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


def run_task(settings_file=DEFAULT_SETTINGS_FILE, asset_id: int = None, measurement_type: list = None, start_date: str = None, end_date: str = None, debug: bool = False) -> bool:

    # Create the client instance
    client = SmartSensorClient(settings_file=settings_file, debug=debug)

    # Authenticate
    if not client.authenticate():
        print('Authentication FAILED')
        return False

    # Print organization
    print('Organization {}, {}'.format(client.organization_id, client.organization_name))
    print()

    # Get the measurement data during this time
    measurements = client.get_measurement_value(asset_id=asset_id,
                                                measurement_type=','.join(str(v) for v in measurement_type),
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
    parser.add_argument('-a', '--asset-id', type=int, help='an integer for the asset ID', required=True)
    parser.add_argument('-m', '--measurement-type', nargs='+',  help='an integer or a list of integers for the measurement types', type=int, required=True)
    parser.add_argument('-s', '--start-date', type=str, help='a string with the start date (YYY-MM-DD)', required=True)
    parser.add_argument('-e', '--end-date', type=str, help='a string with the end date (YYY-MM-DD)', required=True)
    parser.add_argument('-d', '--debug', action='store_true', help='print debug information such as the sent curl request')
    args = parser.parse_args()

    result = run_task(asset_id=args.asset_id, measurement_type=args.measurement_type, start_date=args.start_date, end_date=args.end_date, debug=args.debug)

    if result is True:
        print('Task SUCCESS')
    else:
        print('Task FAILED')
