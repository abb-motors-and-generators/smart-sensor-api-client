# Use Case 3: Change Threshold Values for KPIs

This code demonstrates how to change the threshold values for a specific KPI. A list of four integers defines the thresholds between Healthy, Weak and Critical.

#### Example:
List: 0, 10, 50, 100
- Healthy: 0 - 10
- Weak: 10 - 50
- Critical: 50 - 100 


### Execute
To run this demo, execute the following:

    python use_case_3/change_threshold_values_for_kpis.py -a <ASSET ID> -m <MEASUREMENT TYPE> -v <VALUE LIST>
    
For example, to configure the thresholds such that the measurement type 4 of asset 1234 has threshold values 0, 10, 50 and 100.
    
    python use_case_3/change_threshold_values_for_kpis.py -a 1234 -m 4 -v 0 10 50 100

### Result
<details>
<summary>Sample output - Click to expand!</summary>
<p>

    Changed thresholds of asset 1234 for measurement type 4 to:
    Healthy: 0 to 10
    Weak: 10 to 50
    Critical: 50 to 100
    Task SUCCESS
</p>
</details>


## Settings
If you have not configured your credentials in the `settings.yaml` file in the root folder,
the program will ask you to input your username, password, or API key.
