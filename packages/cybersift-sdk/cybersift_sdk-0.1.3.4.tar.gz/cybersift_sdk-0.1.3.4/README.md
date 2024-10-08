# CyberSift SDK

This is a simple Python SDK for CyberSift Products which provides helper methods to interact with SIEM and Tutela REST APIs.

# SIEM SDK Python Library

## Overview

The SIEM (Security Information and Event Management) SDK is a Python wrapper designed to interact with a SIEM backend. It provides functionalities to manage user authentication and retrieve liveliness data of various agents connected to the system. This library uses Python's `requests` library to interact with a remote SIEM server.


## Installation

```bash
pip install cybersift-sdk
```

## Usage

### Initialization

To initialize the SDK, create an instance of the `SIEM` class. You can provide an optional backend URL (default is `http://localhost:5601`).

```python
from cybersift.siem import SIEM

# Default URL
siem = SIEM()

# Custom backend URL
siem = SIEM(backend="http://your-siem-backend.com")
```

### Functions

#### `login(username: str, password: str, totp: str = "") -> bool`

Authenticates the user with the SIEM backend using a username, password, and optional Time-based One-Time Password (TOTP) for two-factor authentication. Returns `True` on successful login and `False` otherwise.

```python
siem.login(username="admin", password="your_password", totp="123456")
```

**Use Case:**
- **User Authentication:** This method is used to authenticate with the SIEM server before making any subsequent requests.


#### `getDiskUsage() -> List[Dict]`

This function sends a GET request to retrieve disk usage information and returns the response data as a list of dictionaries if the request is successful (200 status code). If the request fails, it prints an error message and returns False.

```python
disk_usage = siem.getDiskUsage()
if disk_usage:
    print(disk_usage)
```

#### `getUptime() -> str`

Returns the SIEM uptime if the request is successful (200 status code). If the request fails, it prints an error message and returns False.

```python
uptime = siem.getUptime()
if disk_usage:
    print(uptime)
```

#### `getAgentLiveliness() -> Union[Dict, bool]`

Fetches the liveliness information of all agents in the SIEM system. Returns a dictionary containing hostnames, their types, last-contact timestamps, and statuses. Returns `False` if the request fails.

```python
liveliness_data = siem.getAgentLiveliness()
if liveliness_data:
    print(liveliness_data)
```

**Use Case:**
- **Monitoring Active Agents:** This method is used to retrieve the status and last contact time of active agents in the SIEM system.

#### `getDeadAgents() -> Union[list, bool]`

Fetches a list of agents that are considered dead (not responsive or have an unknown status). Returns a list of dead agents or `False` if the request fails.

```python
dead_agents = siem.getDeadAgents()
if dead_agents:
    print(dead_agents)
```

**Use Case:**
- **Identifying Dead Agents:** This method helps system administrators monitor and identify agents that are no longer responsive in the SIEM environment.

#### `close()`

Closes the current session.

```python
siem.close()
```

**Use Case:**
- **Session Management:** This method is used to terminate the session once operations are completed to free up resources.

## Example Workflow

```python
from cybersift.siem import SIEM

# Initialize SIEM instance
siem = SIEM()

# Login to the system
if siem.login(username="admin", password="password123", totp=""):
    # Get live agents
    live_agents = siem.getAgentLiveliness()
    if live_agents:
        print("Live Agents:", live_agents)
    
    # Get dead agents
    dead_agents = siem.getDeadAgents()
    if dead_agents:
        print("Dead Agents:", dead_agents)

# Close the session
siem.close()
```

## Error Handling
- If any request fails, a message will be printed with the status code and the response details.

# Tutela SDK Python Library

## Overview

The **Tutela SDK** is a Python library designed to interact with the Tutela backend services for managing assets, retrieving cloud inventory, software information, compliance alerts, and more. It uses Python's `requests` library to communicate with the backend via REST API.

## Installation

```bash
pip install cybersift-sdk
```

## Usage

### Initialization

To initialize the SDK, create an instance of the `Tutela` class. The backend URL can be passed as an optional argument (default is `https://cs-vas-backend.cybersift.io`).

```python
from cybersift.tutela import Tutela

# Default backend URL
tutela = Tutela()

# Custom backend URL
tutela = Tutela(backend="https://your-backend-url")
```

### Functions

#### `login(username: str, password: str) -> bool`

Authenticates the user by performing a login request with the provided username and password. Returns `True` on successful login, `False` otherwise.

```python
tutela.login(username="admin", password="your_password")
```

**Use Case:**
- **User Authentication:** This method logs the user into the backend system to access protected endpoints.

#### `check_login() -> bool`

Checks if the user is currently logged in by making a request to the `/checkLogin` endpoint. Returns `True` if the user is logged in, `False` otherwise.

```python
if tutela.check_login():
    print("User is logged in!")
```

**Use Case:**
- **Session Validation:** This method is used to verify if the current session is authenticated and active.

#### `get_host_agents() -> Union[Dict, bool]`

Fetches the list of host agents (local assets) from the backend. Returns a dictionary of host agents if successful, or `False` if the request fails.

```python
host_agents = tutela.get_host_agents()
if host_agents:
    print(host_agents)
```

**Use Case:**
- **Host Asset Retrieval:** This method retrieves information about all host agents monitored by the system.

#### `get_cloud_assets() -> Union[Dict, bool]`

Fetches the cloud inventory assets by making a request to the backend. Returns a dictionary of cloud assets or `False` if the request fails.

```python
cloud_assets = tutela.get_cloud_assets()
if cloud_assets:
    print(cloud_assets)
```

**Use Case:**
- **Cloud Asset Inventory:** This method retrieves cloud-based assets managed by the system.

#### `get_hosts_with_software(software: str) -> Union[Dict, bool]`

Fetches the hosts that have the specified software installed by searching the asset inventory. Returns a dictionary of hosts that match the search or `False` if the request fails.

```python
hosts_with_software = tutela.get_hosts_with_software(software="nginx")
if hosts_with_software:
    print(hosts_with_software)
```

**Use Case:**
- **Software Search:** This method allows users to search for hosts that have a specific software installed.

#### `get_eol_info() -> Union[Dict, bool]`

Fetches information on End-of-Life (EOL) software. Returns a dictionary containing EOL software details or `False` if the request fails.

```python
eol_info = tutela.get_eol_info()
if eol_info:
    print(eol_info)
```

**Use Case:**
- **EOL Monitoring:** This method provides details about software that has reached its end-of-life.

#### `get_compliance_alerts(query="false") -> Union[Dict, bool]`

Fetches compliance alerts from the backend based on a search query. Returns a dictionary of compliance alerts or `False` if the request fails.

```python
compliance_alerts = tutela.get_compliance_alerts(query="Security")
if compliance_alerts:
    print(compliance_alerts)
```

**Use Case:**
- **Compliance Monitoring:** This method is used to retrieve alerts related to system compliance issues based on specified search criteria.

#### `get_all_compliance_alerts(query="false") -> Union[Dict, bool]`

Fetches all (resolved and pending) compliance alerts from the backend based on a search query. Behaves exactly the same as `get_compliance_alerts()`. Returns a dictionary of compliance alerts or `False` if the request fails. The only difference is that `get_all_compliance_alerts()` will not return any alerts that are resolved, while this method will return all alerts (resolved and pending).

**Use Case:**
- **Audit Compliance Monitoring:** This method is used to retrieve which hosts comply with a best practice and which do not.

#### `close()`

Closes the current session.

```python
tutela.close()
```

**Use Case:**
- **Session Management:** This method is used to close the session once all operations are completed.

## Example Workflow

```python
from cybersift.tutela import Tutela

# Initialize Tutela instance
tutela = Tutela()

# Login to the system
if tutela.login(username="admin", password="password123"):
    # Check login status
    if tutela.check_login():
        print("Logged in!")

    # Get host agents
    host_agents = tutela.get_host_agents()
    if host_agents:
        print("Host Agents:", host_agents)

    # Get cloud assets
    cloud_assets = tutela.get_cloud_assets()
    if cloud_assets:
        print("Cloud Assets:", cloud_assets)

    # Get hosts with specific software
    hosts_with_nginx = tutela.get_hosts_with_software(software="nginx")
    if hosts_with_nginx:
        print("Hosts with NGINX:", hosts_with_nginx)

# Close the session
tutela.close()
```

## Error Handling
- If any request fails, the method prints the status code and the response details to the console.

# Development Guide

```bash
# run test suite
python3 setup.py test

# build for distribution (pip)
python -m build

# upload to pip
twine upload dist/*
```