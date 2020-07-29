# Use Case 2: Show Plant Data

This code demonstrates how to get the information of every plant in the organization

If you have not configured your credentials in the `settings.yaml` file in the root folder,
the program will ask you to input your username, password, or API key.

To run the code, execute:

    python use_case_2_plant_data.py
    
Sample output:

    Organization 1234, Tasty Manufacturing
    
    {'address': 'Smart Street 1, 10001 New York, USA',
     'city': 'New York',
     'country': 'USA',
     'industryTypeID': 3,
     'industryTypeName': 'Other',
     'locationLatitude': '-74.00594130000000000000',
     'locationLongitude': '40.71278370000000000000',
     'organization': {'isPrivateOrgarnization': False,
                      'organizationID': 1234,
                      'organizationName': 'Tasty Manufacturing'},
     'pinNumber': '12345',
     'plantID': 5678,
     'plantName': 'Food Factory',
     'siteIdentifier': None,
     'uniqueID': '1234abcd-1a2b-3c4d-5d6f-abcd1234ffff'}
