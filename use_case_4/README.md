# Use Case 4: Request Condition Indexes of an Asset

This code demonstrates how to get the condition indexes of one or multiple assets.

### Execute

    python  python use_case_4/get_condition_indexes.py <ASSET ID LIST>
    
### Result
<details>
<summary>Sample output - Click to expand!</summary>
<p>

    Asset ID: 1234
    Availability: Good
    Environment: Poor
    Reliability: Good
    Stress: Good
    Overall Condition Index: Good
    
    Asset ID: 5678
    Availability: Good
    Environment: Tolerable
    Reliability: Good
    Stress: Poor
    Overall Condition Index: Good
    Task SUCCESS
</p>
</details>
    
## Settings
If you have not configured your credentials in the `settings.yaml` file in the root folder,
the program will ask you to input your username, password, or API key.
