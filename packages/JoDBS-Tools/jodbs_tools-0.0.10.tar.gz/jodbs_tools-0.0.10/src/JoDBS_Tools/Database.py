import requests
from pymongo import MongoClient, errors
from .utils import Get_ENV

class Database:
    def __init__(self, connection_string=None, collection=None):
        self.connection_string = connection_string or Get_ENV("CONNECTION_STRING")
        self.collection = collection
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.connection_string)
            self.db = self.client[self.collection]
            # print("MongoDB Connection: Successful ✔️")
        except errors.ServerSelectionTimeoutError as err:
            print(f"MongoDB Connection: Failed ❌ - {err}")
            raise Exception("MongoDB Connection: Failed ❌")

    def get_database(self):
        if not self.db:
            self.connect()
        return self.db
    
    def check_status(self):
        try:
            self.client.server_info()
            print("MongoDB Connection: Successful ✔️")
        except errors.ServerSelectionTimeoutError as err:
            print(f"MongoDB Connection: Failed ❌ - {err}")
            raise Exception("MongoDB Connection: Failed ❌")

class BotNetworkConnection:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }

    def get_data(self, application_id, scope="full"):
        url = f"{self.base_url}/data/{application_id}"
        response = requests.get(url, headers=self.headers)

        if scope == "full":
            return self._handle_response(response)
        elif scope == "version":
            data = self._handle_response(response)
            return data.get('data', {}).get('version')
        elif scope == "startup_info":
            data = self._handle_response(response)
            return data.get('data', {}).get('startup_info')
        elif scope == "roles":
            data = self._handle_response(response)
            return data.get('data', {}).get('roles')

    def create_data(self, application_id, data):
        url = f"{self.base_url}/data"
        payload = {
            "applicationId": application_id,
            "data": data
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return self._handle_response(response)

    def update_data(self, application_id, data):
        url = f"{self.base_url}/data/{application_id}"
        payload = {
            "data": data
        }
        response = requests.put(url, headers=self.headers, json=payload)
        return self._handle_response(response)

    def delete_data(self, application_id):
        url = f"{self.base_url}/data/{application_id}"
        response = requests.delete(url, headers=self.headers)
        return self._handle_response(response)

    # def get_startup_info(self, application_id):
    #     url = f"{self.base_url}/"

    def _handle_response(self, response):
        if response.status_code in [200, 201]:
            return response.json()
        else:
            response.raise_for_status()


# class BotNetworkConnection:
#     def __init__(self, api_url=None, token=None):
#         self.api_url = api_url or Get_ENV("API_URL")
#         self.token = token or Get_ENV("API_TOKEN")
#         self.headers = {
#             'Authorization': f'Bearer {self.token}',
#             'Content-Type': 'application/json'
#         }

#     def get_data(self, endpoint):
#         url = f"{self.api_url}/{endpoint}"
#         try:
#             response = requests.get(url, headers=self.headers)
#             response.raise_for_status()
#             print("API Connection: Successful ✔️", self.api_url, endpoint, response.status_code)
#             return response.json()
#         except requests.exceptions.HTTPError as err:
#             print(f"API Connection: Failed ❌ - {err}")
#             raise Exception("API Connection: Failed ❌")
        

    # Get Startup Data from API