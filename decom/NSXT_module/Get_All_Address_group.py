"""
    This module is created to do the API call and get all the raw data related to Device group 
"""
import os
import sys
import json
import urllib3
import requests
from pprint import pprint
from dotenv import load_dotenv
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
from NSXT_module.Core_NSXT import Core_NSXT

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Get_All_Address_group():
    def __init__(self,NSXT_session):
        self.NSXT_session = NSXT_session

    def Address_groups(self):
        try:
            API_request = self.NSXT_session.get(Core_NSXT.Address_Group_get_APIs(), 
                                                    verify = False, 
                                                    timeout = 10)
            API_responce = API_request.json()
            return API_responce
        except Exception as Error:
            msg = {"Error Message": Error}
            return msg

# if __name__ == "__main__":
    
#     NSXT_USERNAME = os.getenv("NSXT_USERNAME")
#     NSXT_PASSWORD = os.getenv("NSXT_PASSWORD")
#     with requests.Session() as NSXT_session:
#         NSXT_session.auth = (NSXT_USERNAME, NSXT_PASSWORD)
#         NSXT_session.verify = False
#         NSXT_session.timeout = 10
#         get_all_raw_address_Group = Get_All_Address_group(NSXT_session)
#         print(get_all_raw_address_Group.Address_groups())
