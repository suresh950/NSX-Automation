# This code will give you the version of NSX firewall
import requests
import urllib3
import sys


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NSXT_IP = "X.X.X.X"
NSXT_USERNAME = "username"
NSXT_PASSWORD = "password"


SNXTSession = requests.Session()
SNXTSession.verify = False  
SNXTSession.auth = (NSXT_USERNAME, NSXT_PASSWORD)

try:
    
    url = f"{NSXT_IP}/api/v1/node/version"
    SNXTGetRequest = SNXTSession.get(url, timeout=10)
    SNXTGetRequest.raise_for_status()

    data = SNXTGetRequest.json()
    version = data.get("product_version", "unknown")
    print(f"Connected to NSX-T successfully (version: {version})")

except requests.exceptions.RequestException as e:
    print(f"Connection failed: {e}")
