# Cloud Interface user guide for ABB AbilityTM Smart Sensors

## Scope

- User guide to learn how to use these [Web APIs](https://api.smartsensor.abb.com/swagger/) for ABB AbilityTM Smart Sensors.
- Provide customers with a simple Python class to communicate with the Smart Sensor Web API. This is a sample project as a starting point to build up the integration project(s).
- Create a community to share new developments, ask questions and propose suggestions for improvements based on real experience.
- For more details, please refer to the [documentation](docs/Cloud_Interface_Open_Guide.pdf).

## Prerequisites

- Python 3 with `pip` and `setuptools` installed
- Test that you have access to the [Smart Sensor Web API](https://api.smartsensor.abb.com/swagger/)
- Obtain an API key from the [Smart Sensor website](https://smartsensor.abb.com)

## Quick Start

1.  Install necessary libraries using `pip`

        pip install -r requirements.txt
    
    Alternatively, install the package using `setuptools` and `pip`
    
        python -m pip install .

2.  Copy `settings.example.yaml` to `settings.yaml` and change the values. You can adjust your proxy settings (leave empty if none).
    You can also optionally specify your API key or username, which the Smart Sensor Client will use automatically.

3.  To run the first example, execute

    ```
    python examples/example_4_latest_asset_measurements.py
    ```
    
3.  To authenticate, enter your API key or your email address and password.

4.  The sample program will display your assets in your Smart Sensor organization and their latest sensor measurements. You can check the measurements against those you see in the [ABB AbilityTM Smart Sensor Platform](https://smartsensor.abb.com).

5.  Finally, you can look at the [source code](examples/example_4_latest_asset_measurements.py) and [SmartSensorClient](smart_sensor_client/smart_sensor_client.py) to see how it uses the Cloud Interface and how you can adapt it for your integration project.

## Examples

We provide the following examples to access the Smart Sensor Cloud Interface.
You can run the script by executing

    python examples/<example_file_name>

| Name                                   | Explanation                                      | 
|----------------------------------------|--------------------------------------------------|
| example_1_list_of_assets.py            | Show the information of all the assets           |
| example_2_plant_data.py                | Show the information of all the plants           |
| example_3_detailed_asset_data.py       | Show the detailed information of all the assets  |
| example_4_latest_asset_measurements.py | Show the latest measurements from all the assets |
