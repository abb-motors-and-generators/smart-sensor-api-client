# Use Case 1: Show All Asset Information

This code show the information of all the assets belonging to the user's current organization.

If you have not configured your credentials in the `settings.yaml` file in the root folder,
the program will ask you to input your username, password, or API key.

To run the code, execute:

    python use_case_1_list_of_assets.py
    
Sample output:

    Organization 1234, Tasty Manufacturing
    
    Plant 5678, Food Factory:
    Assets:
    {'assetGroupID': 1000,
     'assetID': 2000,
     'assetName': 'Motor 1',
     'assetResponsibleID': None,
     'assetResponsibleName': None,
     'assetType': {'assetTypeID': 1, 'assetTypeName': 'Motor'},
     'configurationProfileID': 3,
     'configurationProfileName': 'Motor Profile',
     'createdOn': '2018-01-12T16:23:45.931',
     'description': None,
     'healthStatus': {'healthCode': 'Healthy', 'healthColor': '#21BE89'},
     'isFavourite': False,
     'isPowerTrainComponent': False,
     'lastSyncTimeStamp': '2018-01-13T16:23:45.931',
     'lastUpdatedOn': '2018-01-14T16:23:45.931',
     'locationLatitude': '',
     'locationLongitude': '',
     'organization': {'isPrivateOrgarnization': False,
                      'organizationID': 1234,
                      'organizationName': 'Tasty Manufacturing'},
     'plantID': 5678,
     'plantName': 'Food Factory',
     'sensorIdentifier': 'S2A0000001-ABCD',
     'sensorTypeID': 1,
     'serialNumber': '10',
     'siteIdentifier': None}