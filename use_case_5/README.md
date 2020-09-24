# Use Case 5: Request Measurement Data of an Asset	

With this use case, you can fetch measurement data from sensors. You can get the latest measurement or also a series of measurements and plot them in time.


## Plot History Measurement Data 
This code will plot values of defined measurement types in a defined date range of a chosen asset.

### Execute
To run this demo, execute the following:

    python use_case_5/get_historic_measurements.py -a <ASSET ID LIST> -m <MEASUREMENT TYPE> -s <START DATE> -e <END DATE>
    
For example, to get the skin temperature measurements (measurement type 4) from the assets 1234 and 4567 in the time range of 2020-01-01 until 2020-02-01 you can execute:
    
    python use_case_5/get_historic_measurements.py -a 1234 4567 -m 4 -s 2020-01-01 -e 2020-02-01
    
### Result
<details>
<summary>Sample output - Click to expand!</summary>
<p>

    Organization 1234, Tasty Manufacturing

    Task SUCCESS
  
![Example Measurement Plot](example_measurement_plot.png "Example Measurement Plot")

</p>
</details>


## Get Latest Measurement
This code shows the latest measurements of all the assets belonging to the user's current organization.

### Execute
To run this demo, execute the following script:

     python use_case_5/get_latest_measurements.py
    
### Result

<details>
<summary>Sample output - Click to expand!</summary>
<p>
    
    Organization 1234, Tasty Manufacturing
    
    Plant 5678, Food Factory:
    Assets:
    Latest measurements of Asset 2000, Motor 1:
          Speed                                : 0.0000 (2018-01-13T16:23:45)
          Skin Temperature                     : 30.1234 (2018-01-13T16:23:45)
          Overall Vibration                    : 0.0123 (2018-01-13T16:23:45)
          Operating Time                       : 320.0000 (2018-01-13T16:23:45)
          Number of Starts                     : 3.0000 (2018-01-13T16:23:45)
          Motor Supply Frequency               : 50.0000 (2018-01-13T16:23:45)
          Bearing Condition                    : 0.0000 (2018-01-13T16:23:45)
          Vibration (Radial)                   : 0.0123 (2018-01-13T16:23:45)
          Vibration (Tangential)               : 0.0456 (2018-01-13T16:23:45)
          Vibration (Axial)                    : 0.0789 (2018-01-13T16:23:45)
          Output Power                         : 0.0000 (2018-01-13T16:23:45)

</p>
</details>

## Settings
If you have not configured your credentials in the `settings.yaml` file in the root folder,
the program will ask you to input your username, password, or API key.
