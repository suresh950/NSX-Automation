import requests
import urllib3
import sys
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NSXT_USERNAME = "username"
NSXT_PASSWORD = "password"
BASE_URL = "ip of nsxt Firewall"

with requests.Session() as NSXT_session:
    NSXT_session.auth = (NSXT_USERNAME, NSXT_PASSWORD)
    NSXT_session.verify = False
    NSXT_session.timeout=10
    API_request = NSXT_session.get(f'{BASE_URL}/api/v1/node/version')
# /policy/api/v1/global-infra/domains/{domain-id}/groups
# /policy/api/v1/infra/domains/{domain-id}/groups
print(API_request.json())

with open("raw_data_12.json", "w") as f:
    json.dump(API_request.json() , f , indent=4)
