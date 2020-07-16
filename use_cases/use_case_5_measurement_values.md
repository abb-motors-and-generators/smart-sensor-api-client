# Use Case 5: Plot Measurement Values from Chosen Asset	

This code will plot values of defined measurement types in a defined date range of a chosen asset.

If you have not configured your credentials in the `settings.yaml` file in the root folder,
the program will ask you to input your username, password, or API key.

To run the code, execute:

     python use_case_5_measurement_values.py
    
<details>
  <summary>Sample output - Click to expand!</summary>
    
    Organization 1234, Tasty Manufacturing

    Please enter your query parameters:
    Asset ID: 2000
    Measurement type (4 for temperature): 4
    Start date (YYYY-MM-DD): 2019-02-15
    End date (YYYY-MM-DD): 2019-06-15
    Task SUCCESS
    
![Example Measurement Plot](../example_measurement_plot.png "Example Measurement Plot")

</details>
