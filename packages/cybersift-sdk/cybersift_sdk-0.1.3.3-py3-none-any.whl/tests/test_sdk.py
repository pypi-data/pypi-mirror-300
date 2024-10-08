import unittest
import os

from dotenv import load_dotenv
from cybersift.siem import SIEM
from cybersift.tutela import Tutela

# Load the .env file
load_dotenv()

TEST_USERNAME = os.getenv('TUTELA_USERNAME') 
TEST_PASSWORD = os.getenv('TUTELA_PASSWORD') 

TEST_SIEM_USERNAME = os.getenv('SIEM_USERNAME') 
TEST_SIEM_PASSWORD = os.getenv('SIEM_PASSWORD') 

class TestSdkModule(unittest.TestCase):
    def test_successful_login(self):
        tutela = Tutela(backend="https://trial-backend.tutela.cybersift.io")
        tutela.login(TEST_USERNAME, TEST_PASSWORD)        
        result = tutela.check_login()        
        tutela.close()
        self.assertTrue(result)

    def test_unsuccessful_login(self):
        tutela = Tutela(backend="https://trial-backend.tutela.cybersift.io")
        tutela.login(TEST_USERNAME, '')        
        result = tutela.check_login()        
        tutela.close()
        self.assertFalse(result)

    def test_get_host_agents(self):
        tutela = Tutela(backend="https://trial-backend.tutela.cybersift.io")
        tutela.login(TEST_USERNAME, TEST_PASSWORD)
        result = tutela.get_host_agents()
        tutela.close()
        self.assertTrue(len(result) > 0)

    def test_get_cloud_assets(self):
        tutela = Tutela(backend="https://trial-backend.tutela.cybersift.io")
        tutela.login(TEST_USERNAME, TEST_PASSWORD)
        result = tutela.get_cloud_assets()
        tutela.close()
        self.assertTrue(len(result) > 0)

    def test_get_hosts_with_imaginary_software(self):
        tutela = Tutela(backend="https://trial-backend.tutela.cybersift.io")
        tutela.login(TEST_USERNAME, TEST_PASSWORD)
        result = tutela.get_hosts_with_software("basssaasasas")
        tutela.close()
        self.assertTrue(len(result) == 0)

    def test_get_hosts_with_real_software(self):
        tutela = Tutela(backend="https://trial-backend.tutela.cybersift.io")
        tutela.login(TEST_USERNAME, TEST_PASSWORD)
        result = tutela.get_hosts_with_software("chrome")        
        tutela.close()
        self.assertTrue(len(result) > 0)

    def test_get_software_version(self):
        tutela = Tutela(backend="https://trial-backend.tutela.cybersift.io")
        tutela.login(TEST_USERNAME, TEST_PASSWORD)
        hosts = tutela.get_hosts_with_software("chrome")        
        result = hosts[0]['Packages'][0]['Version']
        print(result)
        tutela.close()
        self.assertTrue(len(result) > 0)

    def test_get_eol(self):
        tutela = Tutela(backend="https://trial-backend.tutela.cybersift.io")
        tutela.login(TEST_USERNAME, TEST_PASSWORD)
        result = tutela.get_eol_info()
        tutela.close()
        self.assertTrue(len(result) > 0)

    def test_get_imaginary_compliance_alerts(self):
        tutela = Tutela(backend="https://trial-backend.tutela.cybersift.io")
        tutela.login(TEST_USERNAME, TEST_PASSWORD)
        result = tutela.get_compliance_alerts("direct-abc-access")
        tutela.close()
        self.assertTrue(len(result) == 0)
        
    def test_get_real_compliance_alerts(self):
        tutela = Tutela(backend="https://trial-backend.tutela.cybersift.io")
        tutela.login(TEST_USERNAME, TEST_PASSWORD)
        result = tutela.get_compliance_alerts("direct-internet-access")
        tutela.close()
        self.assertTrue(len(result) > 0)

    def test_get_all_real_compliance_alerts(self):
        tutela = Tutela(backend="https://trial-backend.tutela.cybersift.io")
        tutela.login(TEST_USERNAME, TEST_PASSWORD)
        result = tutela.get_all_compliance_alerts("direct-internet-access")
        print("Host: " + result[0]['Host']['Hostname'])
        print("Resolved: " + str(result[0]['Resolved']))
        tutela.close()
        self.assertTrue(len(result) > 0)

    def test_siem_good_login(self):
        siem = SIEM(backend="http://localhost:5601")
        result = siem.login(TEST_SIEM_USERNAME, TEST_SIEM_PASSWORD)
        self.assertTrue(result)

    def test_siem_bad_login(self):
        siem = SIEM(backend="http://localhost:5601")
        result = siem.login(TEST_SIEM_USERNAME, '')
        self.assertFalse(result)

    def test_siem_agent_liveliness(self):
        siem = SIEM(backend="http://localhost:5601")
        siem.login(TEST_SIEM_USERNAME, TEST_SIEM_PASSWORD)
        result = siem.getAgentLiveliness()
        print(result)
        self.assertTrue(len(result) > 0)

    def test_siem_disk_usage(self):
        siem = SIEM(backend="http://localhost:5601")
        siem.login(TEST_SIEM_USERNAME, TEST_SIEM_PASSWORD)
        result = siem.getDiskUsage()
        print(result)
        self.assertTrue(len(result) > 0)

    def test_siem_uptime(self):
        siem = SIEM(backend="http://localhost:5601")
        siem.login(TEST_SIEM_USERNAME, TEST_SIEM_PASSWORD)
        result = siem.getUptime()
        print(result)
        self.assertTrue(len(result) > 0)


    def test_siem_dead_agents(self):
        siem = SIEM(backend="http://localhost:5601")
        siem.login(TEST_SIEM_USERNAME, TEST_SIEM_PASSWORD)
        result = siem.getDeadAgents()
        print(result)
        self.assertTrue(len(result) > 0)


if __name__ == "__main__":
    unittest.main()