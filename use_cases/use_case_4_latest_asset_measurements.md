# Use Case 4: Show Latest Measurements from All Assets	

This code shows the latest measurements of all the assets belonging to the user's current organization.

If you have not configured your credentials in the `settings.yaml` file in the root folder,
the program will ask you to input your username, password, or API key.

To run the code, execute:

    python use_case_4_latest_asset_measurements.py
    
Sample output:

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
