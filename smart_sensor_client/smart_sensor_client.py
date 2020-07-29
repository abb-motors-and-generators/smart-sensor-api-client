import json
import requests
import logging
import yaml
from getpass import getpass
import curlify


class SmartSensorClient:
    """Simple client library to access the Smart Sensor API.

    This Python class acts as an example of how to create a custom library to interface with the Smart Sensor Web API.
    The user should first initiate the class object and call authenticate().

    Attributes:
        url: The URL for the Smart Sensor API
        api_key: The API key used for authentication
        auth_token: The authentication token used for all subsequent requests
        organization_id: The unique organization ID that the current user belongs to
    """

    DEFAULT_API_URL = 'https://api.smartsensor.abb.com/'

    def __init__(self, settings_file: str = '', debug: bool = False):
        """Initializes SmartSensorAPIClient

        Args:
            url: the URL of the web API
            proxy: the proxy server, in the format of proxy.server.com:port_number
        """

        # Set up logger
        logging.basicConfig()
        self._logger = logging.getLogger(__class__.__name__)

        # Set the API URL
        self.url = self.DEFAULT_API_URL

        # Initialize other variables
        self.api_key = None
        self.username = None
        self.auth_info = None
        self.auth_token = None
        self.is_super_admin = None
        self.organization_id = None
        self.organizations = None
        self.plants = None
        self.assets = dict()
        self.proxies = dict()

        # Parse the settings file
        self.configure(settings_file)
        self.debug = debug

    def configure(self, settings_file):
        """Configures the client using a config file

        Args:
            settings_file: the path of the config file, relative or absolute

        """
        with open(settings_file) as stream:
            try:
                configs = yaml.safe_load(stream)

                if configs.get('debug') is True:
                    self._logger.setLevel(logging.DEBUG)

                if 'proxy' in configs:
                    self.proxies = {'https': configs['proxy']}

                # Copy the authentication information
                self.api_key = configs.get('api_key')
                self.username = configs.get('username')

            except yaml.YAMLError as e:
                print(e)

    def authenticate_key(self, key) -> bool:
        """Authenticates using a API key

        Args:
            key: the API key

        Returns:
            bool: True for successful authentication. False otherwise.

        """

        # Keep a copy of the key
        self.api_key = key

        # Set up the parameters for the request
        parameters = {'deviceUID': 'string', 'apiKey': self.api_key}

        # Issue the request
        response = requests.post(self.url + 'Auth/Key', json=parameters, proxies=self.proxies)

        # Parse the response and return success or failure
        return self._parse_authentication_response(response)

    def authenticate_password(self, username, password=None) -> bool:
        """Authenticates using a username and its password

        Args:
            username: the user name in email format
            password: the password

        Returns:
            bool: True for successful authentication. False otherwise.

        """

        # Keep a copy of the username
        self.username = username

        if password is None:
            password = getpass('Please enter your password: ')

        # Set up the parameters for the request
        parameters = {'deviceUID': 'string', 'userName': username, 'password': password}

        # Issue the request
        response = requests.post(self.url + 'Auth', json=parameters, proxies=self.proxies)

        # Parse the response and return success or failure
        return self._parse_authentication_response(response)

    def _parse_authentication_response(self, response) -> bool:
        """Parses the server response to the authentication request

        Args:
            response: the response from request.post()

        Returns:
            bool: True for successful authentication. False otherwise.

        """

        if response.status_code != 200:
            self._logger.error('{}:{}'.format(response.status_code, response.reason))
            return False

        # Convert response to json format
        response_json = json.loads(response.content)

        # Store authentication info
        self.auth_info = response_json

        # Store authentication token
        self.auth_token = response_json['authToken']

        # Store organization info of the current user
        self.organization_id = response_json['organizationID']
        self.organization_name = response_json['organizationName']

        # Store the admin state
        self.is_super_admin = response_json['isSuperAdmin']

        return True

    def authenticate(self):
        """Authenticates the user based on the whether the API key or username is available

        Returns:
            bool: True for successful authentication. False otherwise.

        """

        if self.api_key is not None:  # First try to use the API key
            return self.authenticate_key(self.api_key)
        elif self.username is not None:  # Then try to use the user email
            return self.authenticate_password(username=self.username)
        else:  # Read the key/name from the commandline and call authenticate_key or authenticate_password
            value = str(input('Please enter your email or API key: '))
            if '@' in value:  # Use username/password authentication if the user entered email
                return self.authenticate_password(username=value)
            else:  # use API key authentication if user entered key
                return self.authenticate_key(key=value)

    def authenticate_old(self, key=None, username=None, password=None, interactive=False):
        """Authenticates to the API server using the API key and obtain the auth token and organization ID."""

        parameters = dict()
        parameters['deviceUID'] = 'string'

        # If using API key
        if key is not None:
            # Save the key
            self.api_key = key

            # Set up parameters for the request
            parameters['apiKey'] = self.api_key

            # Issue the request
            response = requests.post(self.url + 'Auth/Key', json=parameters, proxies=self.proxies)

        elif username is not None and password is not None:
            # Set up parameters for the request
            parameters['userName'] = username
            parameters['password'] = password

            # Issue the request
            response = requests.post(self.url + 'Auth', json=parameters, proxies=self.proxies)

        # If the request resulted in an error, raise an exception
        if response.status_code != 200:
            raise Exception('Error:', str(response.status_code), response.reason)

        # Convert response to json format
        response_json = json.loads(response.content)

        # Store authentication info
        self.auth_info = response_json

        # Store authentication token
        self.auth_token = response_json['authToken']

        # Store organization ID because it is unique to the current user
        self.organization_id = response_json['organizationID']

        # Store the admin state
        self.is_super_admin = response_json['isSuperAdmin']

        return response_json

    def get_organizations(self):
        """"Get the list of organizations"""

        # If there is already a list, return it
        if len(self.organizations) != 0:
            return self.organizations

        # If the user is a super admin, use the Organization API
        if self.is_super_admin:
            reply = self.get_request('Organization', {})
        # Otherwise, get the list from the history of the user's organizations
        else:
            reply = self.get_request('User/OrganizationHistory', {})

        # Extracting the organization information
        self.organizations.clear()
        for r in reply:
            o = {k: r[k] for k in ('organizationID', 'organizationName')}
            self.organizations.append(o)

        self.organizations = sorted(self.organizations, key=lambda k: k['organizationID'])

        return self.organizations

    def set_organization_id(self, organization_id):
        """Set the working organization ID"""

        # Get all organizations
        organizations = self.get_organizations()

        # Find the organization's ID by its name
        for o in organizations:
            if o['organizationID'] == organization_id:
                organization_name = o['organizationName']
                self.set_organization(organization_name)
                return True

        # Return false if there is no matching organization ID
        return False

    def set_organization(self, organization_name):
        """Set the working organization Name"""

        params = {'organizationName': organization_name}
        reply = self.put_request('User/Organization', params)
        if len(reply) == 0:
            return False

        self.organization_id = reply['organizationID']
        return True

    def get_organization_id(self):
        """Get the working organization ID"""
        return self.organization_id

    def get_plants(self, organization_id=None):
        """Gets all plants in an organization"""

        # If there was no specified organization_id, use the currently selected one
        if organization_id is None:
            print('Using default organization', self.organization_id)
            organization_id = self.organization_id

        # Error handling, if the organization is not found
        if self.is_super_admin:
            organization_info = self.api_organization_info(organization_id)
            if organization_info is None:
                print('Error: organization', organization_id, 'not found')
                return []
        else:
            organizations = self.get_organizations()
            a = [o['organizationID'] for o in organizations]
            if organization_id not in a:
                print('Error: organization', organization_id, 'not found')
                return []

        # If the plants in this organization are not fetched yet, fetch them
        if organization_id not in self.plants:
            # Read from the API
            parameters = dict()
            parameters['organizationID'] = organization_id
            reply = self.get_request('Plant', parameters)
            if reply is None:
                return None

            # If the reply is non-empty parse the reply and add to the list
            # Create new list for this organization
            self.plants[organization_id] = list()
            for r in reply:
                o = {k: r[k] for k in ('plantID', 'plantName')}
                self.plants[organization_id].append(o)

        # Return the plant list of the organization
        return self.plants[organization_id]

    def get_assets(self, organization_id=None, plant_id=None):
        """"Gets all assets from a given plant"""

        if organization_id is None:
            organization_id = self.organization_id

        if plant_id is None:
            plant_id = ''

        # If the assets are not fetched before, fetch them
        if plant_id not in self.assets:
            # Issue the request
            assets = self.get_asset_list(organization_id=organization_id, plant_id=plant_id)
            self.assets[plant_id] = assets

        return self.assets[plant_id]

    def api_organization_info(self, organization_id):
        """"Gets the organization information"""
        reply = self.get_request('Organization/' + str(organization_id), {})
        if reply is None or 'organizationID' not in reply:
            return None
        return reply

    def api_plant_info(self, plant_id):
        """"Gets the plant information"""
        reply = self.get_request('Plant/' + str(plant_id), {})
        return reply

    def asset_get_asset_by_id(self, asset_id):
        """Gets asset extended data.

        :param asset_id: the asset ID
        :return: the asset extended data
        """
        reply = self.get_request('Asset/' + str(asset_id), feature_code='EXT_ViewAssetDetails')
        return reply

    def asset_get_asset_data(self, asset_id):
        """Gets asset data

        :param asset_id: the asset ID
        :return: the asset extended data
        """
        reply = self.get_request('Asset/Data/' + str(asset_id), {})
        return reply

    def get_asset_list(self, organization_id=None, plant_id=None, asset_group_id=None):
        """Gets the list of assets in organization. You can optionally specify the plant ID and asset group ID"""
        parameters = {}
        if organization_id is not None:
            parameters['organizationID'] = organization_id
        else:
            parameters['organizationID'] = self.organization_id
        if plant_id is not None:
            parameters['plantID'] = plant_id
        if asset_group_id is not None:
            parameters['assetGroupID'] = asset_group_id

        reply = self.get_request('Asset/List', parameters)

        # Parse reply
        assets = []
        for r in reply:
            # o = {k: r[k] for k in ('sensorTypeID', 'sensorIdentifier', 'assetID', 'assetName', 'serialNumber', 'description', 'assetGroupID')}
            # assets.append(o)
            assets.append(r)

        return assets

    def get_plant_list(self):
        """Gets the list of plants belonging to the organization ID"""
        parameters = {}
        parameters['organizationID'] = self.organization_id
        return self.get_request('Plant', parameters)

    def get_measurement_types(self, asset_id):
        """Gets all possible measurement types of an asset"""
        parameters = {}
        # receive the asset data to find out the asset type ID of the chosen asset
        asset_data = self.asset_get_asset_data(asset_id)
        # extract assetTypeID from the received data
        parameters['assetTypeID'] = asset_data['assetType']['assetTypeID']
        return self.get_request('Measurement/AssetType', parameters)

    def get_asset_measurement(self, asset_id):
        """Gets one single measurement of an asset"""
        parameters = {}
        return self.get_request('Asset/Measurement/' + str(asset_id), parameters)

    def get_measurement_value(self, asset_id, measurement_type, start_time, end_time):
        """Gets historical data of an asset of a measurement time and a time range"""
        parameters = {}
        parameters['assetID'] = asset_id
        parameters['measurementTypes'] = measurement_type
        parameters['from'] = start_time
        parameters['to'] = end_time
        return self.get_request('Measurement/Value', parameters)

    def add_notification_channel(self, id, channel_id, asset_id_list, url):
        # This endpoint requires data as an application/json content type
        content_type = 'application/json-patch+json'
        parameters = dict()
        parameters["assetIDList"] = asset_id_list
        parameters["properties"] = [
            {
                "key": "verb",
                "value": "POST"
            },
            {
                "key": "path",
                "value": url
            },
        ]
        parameters["template"] = """{ 
                \"type\": id, 
                \"content\": { 
                    \"assetID\": {AssetID},
                    \"assetName\": \"{AssetName}\",
                    \"organizationID\": {AssetOrganizationID},
                    \"organizationName\": \"{AssetOrganizationName}\" } 
                }"""

        return self.put_request('Notification/Asset/Channel/' + str(id) + '?channelID=' + str(channel_id), parameters,
                                content_type=content_type)

    def get_condition_index(self, asset_id):
        """Gets condition indexes of an asset or an asset list"""
        data = []
        data.extend(asset_id)
        return self.post_request('ConditionIndex', data=data)

    def get_request(self, api, parameters=None, feature_code=None):
        """Worker function to perform the GET request"""

        # If the feature code was not provided, try to find it
        if feature_code is None:
            feature_code = self.get_feature_code(api)

        # Set up headers
        headers = dict()
        if self.auth_token is not None:
            headers['Authorization'] = 'Bearer ' + self.auth_token
        if feature_code is not None:
            headers['FeatureCode'] = feature_code

        # Set up the URL
        url = self.url + api

        # Send the request and get the response
        response = requests.get(url, headers=headers, params=parameters, proxies=self.proxies)

        # Print curl request
        if self.debug:
            print('Sent curl request:')
            print(curlify.to_curl(response.request))

        # Parse the response into json format
        response_json = json.loads(response.content)

        # Return None if the response code indicates an error
        if response.status_code != 200:
            print('Error: Response Code', str(response.status_code), response_json)
            # print('URL:', url)
            # print('parameters:', parameters)
            # print('headers:', headers)
            # print()
            return None

        return response_json

    def post_request(self, api, data, feature_code=None, content_type=None):
        """Worker function to perform the POST request"""

        # If the feature code was not provided, try to find it
        if feature_code is None:
            feature_code = self.get_feature_code(api)

        # Set up headers
        headers = dict()
        if self.auth_token is not None:
            headers['Authorization'] = 'Bearer ' + self.auth_token
        if feature_code is not None:
            headers['FeatureCode'] = feature_code
        if content_type is not None:
            headers["Content-Type"] = content_type

        # Set up the URL
        url = self.url + api

        # Send the request and get the response
        response = requests.post(url, headers=headers, json=data, proxies=self.proxies)

        # Print curl request
        if self.debug:
            print('Sent curl request:')
            print(curlify.to_curl(response.request))

        if response.status_code != 200:
            print('Error: Response Code', str(response.status_code))
            return False

        # Print the JSON response
        if response.text:
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                txt = f"Unable to decode response content: ({response.text})"
                print(txt)

        return True

    def put_request(self, api, data, feature_code=None, content_type=None):
        """Worker function to perform the PUT request"""

        # If the feature code was not provided, try to find it
        if feature_code is None:
            feature_code = self.get_feature_code(api)

        # Set up headers
        headers = dict()
        if self.auth_token is not None:
            headers['Authorization'] = 'Bearer ' + self.auth_token
        if feature_code is not None:
            headers['FeatureCode'] = feature_code
        if content_type is not None:
            headers["Content-Type"] = content_type

        # Set up the URL
        url = self.url + api

        # Send the request and get the response
        str_data = json.dumps(data)
        response = requests.put(url, headers=headers, data=str_data, proxies=self.proxies)

        # Print curl request
        if self.debug:
            print('Sent curl request:')
            print(curlify.to_curl(response.request))

        if response.status_code != 200:
            print('Error: Response Code', str(response.status_code))
            return False

        # Print the JSON response
        if response.text:
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                txt = f"Unable to decode response content: ({response.text})"
                print(txt)

        return True

    @staticmethod
    def get_feature_code(api):
        """Automatically fill in known feature codes based on the API accessed"""
        if api == 'Asset/List':
            feature_code = 'EXT_ListAssets'
        elif api == 'Asset/':
            print('Using EXT_ViewAssetDetails')
            feature_code = 'EXT_ViewAssetDetails'
        elif api == 'Measurement/HealthInterval':
            feature_code = 'EXT_ConfigureAssetHealth'
        elif 'ConditionIndex' in api:
            feature_code = 'EXT_AssetConditionIndex'
        elif 'EventLog' in api:
            feature_code = 'EXT_AssetEventLog'
        elif api == 'Measurement/Value':
            feature_code = 'EXT_AssetTrendData'
        else:
            feature_code = None
        return feature_code
