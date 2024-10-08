import requests
from typing import Union, Dict


class SIEM():

    def __init__(self, backend = "http://localhost:5601", session = None):
        # Initialize a requests session on class instantiation
        if session:
            self.session = session
        else:
            self.session = requests.Session()
        self.session.headers.update({"osd-xsrf": "sdk"})
        self.url = backend
        print("SIEM SDK Session initialized!")

    def login(self, username: str, password: str, totp: str = ""):
        
        payload = {
            'username': username,
            'password': password,
            #'otp'     : totp
        }
        
        # Perform the POST request to the given URL
        response = self.session.post(f"{self.url}/auth/login", data=payload)
        
        if response.status_code == 200:
            print("Login successful!")
            # Cookies will automatically be stored in the session object
            return True
        elif response.status_code == 400 and response.json()["message"].startswith("[request body.otp]"):
            payload['otp'] = totp
            response = self.session.post(f"{self.url}/auth/login", data=payload)
            if response.status_code == 200:
                print("Login successful!")
                return True

        print(f"Login failed with status code: {response.status_code} response: {response.text}")
        return False
        
    def getAgentLiveliness(self) -> Union[Dict, bool]:
        response = self.session.get(f"{self.url}/cs_api/system/liveliness")

        if response.status_code == 200:
            hosts = []
            json_data = response.json()
            for type in json_data:
                for hostname in json_data[type]:
                    host = json_data[type][hostname]
                    if "status" not in host:
                        hosts.append({
                            "hostname": hostname, 
                            "type": type, 
                            "last-contact": "unknown",
                            "status": "unknown",
                            "hours": -1
                        })
                        
                    else:
                        hosts.append({
                            "hostname": hostname, 
                            "type": type, 
                            "last-contact": host["last-contact"],
                            "status": host["status"],
                            "hours": float(host["last-contact"].replace("hours ago", ""))
                        })

            return hosts
        else:
            print(f"Request failed with status code: {response.status_code}, response: {response.text}")
            return False
        
    def getUptime(self) -> str:
        response = self.session.get(f"{self.url}/cs_api/system/uptime")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}, response: {response.text}")
            return False

    def getDiskUsage(self) -> list[dict]:
        response = self.session.get(f"{self.url}/cs_api/system/disk")

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}, response: {response.text}")
            return False
        

    def getDeadAgents(self) -> Union[list, bool]:
        response = self.session.get(f"{self.url}/cs_api/system/liveliness")

        if response.status_code == 200:
            dead_hosts = []
            json_data = response.json()
            for type in json_data:
                for hostname in json_data[type]:
                    host = json_data[type][hostname]
                    if "status" not in host:
                        dead_hosts.append({
                            "hostname": hostname, 
                            "type": type, 
                            "last-contact": "unknown",
                            "hours": -1
                        })
                        
                    elif host["status"] != "OK":
                        dead_hosts.append({
                            "hostname": hostname, 
                            "type": type, 
                            "last-contact": host["last-contact"],
                            "hours": float(host["last-contact"].replace("hours ago", ""))
                        })

            return dead_hosts
        else:
            print(f"Request failed with status code: {response.status_code}, response: {response.text}")
            return False

    def close(self):
        # Close the session
        self.session.close()
        print("Session closed!")