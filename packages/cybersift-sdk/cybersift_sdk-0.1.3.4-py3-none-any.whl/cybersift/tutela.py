import requests
from typing import Union, Dict


class Tutela():

    def __init__(self, backend = "https://cs-vas-backend.cybersift.io"):
        # Initialize a requests session on class instantiation
        self.session = requests.Session()
        self.url = backend
        print("Tutela SDK Session initialized!")

    def login(self, username: str, password: str):
        # Method to perform a POST request to "/login"
        payload = {
            'Username': username,
            'Password': password
        }
        
        # Perform the POST request to the given URL
        response = self.session.post(f"{self.url}/userLogin", data=payload)
        
        if response.status_code == 200:
            print("Login successful!")
            # Cookies will automatically be stored in the session object
            return True
        else:
            print(f"Login failed with status code: {response.status_code}")
            return False
        
    def check_login(self):
        # Method to check if the user is logged in
        response = self.session.post(f"{self.url}/checkLogin")

        if response.status_code == 200:
            print("User is logged in!")
            return True
        else:
            print("User is not logged in!")
            return False
        
    def get_host_agents(self) -> Union[Dict, bool]:
        response = self.session.get(f"{self.url}/retrieveHostAssets")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}, response: {response.text}")
            return False
        
    def get_cloud_assets(self) -> Union[Dict, bool]:
        response = self.session.post(f"{self.url}/retrieveCloudInventoryResults")

        if response.status_code == 200:
            return response.json()['Results']
        else:
            print(f"Request failed with status code: {response.status_code}, response: {response.text}")
            return False
        
    def get_hosts_with_software(self, software) -> Union[Dict, bool]:
        response = self.session.post(f"{self.url}/retrieveAssetsV2/all/-1", json={
            "addressFilter": "false",
            "osFilter": "false",
            "packageFilter": "false",
            "portFilter": "false",
            "serviceFilter": "false",
            "searchQuery": software,
            "packageAnomaly": "false",
            "packageInstall": "installed",
            "serviceShowRecent": 0,
            "showTcpWrapped": "false",
            "showOnlyOutdated": "false"
        })

        if response.status_code == 200:
            return response.json()['Hosts']
        else:
            print(f"Request failed with status code: {response.status_code}, response: {response.text}")
            return False

    def get_eol_info(self) -> Union[Dict, bool]:
        response = self.session.get(f"{self.url}/eol/retrieveEolSoftware")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}, response: {response.text}")
            return False
        
    def get_compliance_alerts(self, query="false") -> Union[Dict, bool]:
        response = self.session.post(f"{self.url}/getComplianceAlerts", json={
            "PageIndex": 0,
            "PageSize": -1,
            "SortField": "Hostname",
            "SortDirection": "desc",
            "Filters": {
                "Severity": "false",
                "StigID": "false",
                "Host": "false",
                "SearchQuery": query,
                "Status": "Pending"
            }
        })

        if response.status_code == 200:
            return response.json()['ComplianceAlerts']
        else:
            print(f"Request failed with status code: {response.status_code}, response: {response.text}")
            return False
        
    def get_all_compliance_alerts(self, query="false") -> Union[Dict, bool]:
        response = self.session.post(f"{self.url}/getComplianceAlerts", json={
            "PageIndex": 0,
            "PageSize": -1,
            "SortField": "Hostname",
            "SortDirection": "desc",
            "Filters": {
                "Severity": "false",
                "StigID": "false",
                "Host": "false",
                "SearchQuery": query,
                "Status": "false"
            }
        })

        if response.status_code == 200:
            return response.json()['ComplianceAlerts']
        else:
            print(f"Request failed with status code: {response.status_code}, response: {response.text}")
            return False


    def close(self):
        # Close the session
        self.session.close()
        print("Session closed!")