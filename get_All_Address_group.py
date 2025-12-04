"""
    This module is created to do the API call and get all the raw data related to Device group 
"""
from pprint import pprint
import requests
import urllib3
import json
import sys
import os
from dotenv import load_dotenv
load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Get_All_Address_group():
    def __init__(self,NSXT_USERNAME,NSXT_PASSWORD,BASE_URL,DOMAIN_ID):
        self.NSXT_USERNAME = NSXT_USERNAME
        self.NSXT_PASSWORD = NSXT_PASSWORD
        self.BASE_URL = BASE_URL
        self.DOMAIN_ID = DOMAIN_ID

    def Address_groups(self):
        try:
            with requests.Session() as NSXT_session:
                NSXT_session.auth = (self.NSXT_USERNAME,self.NSXT_PASSWORD)
                NSXT_session.verify = False
                NSXT_session.timeout = 10
                API_request = NSXT_session.get(f'{self.BASE_URL}/policy/api/v1/infra/domains/{self.DOMAIN_ID}/groups', 
                                                        verify = False, 
                                                        timeout = 10)
            API_responce = API_request.json()
            print("Get the API responce")
            return API_responce
        except Exception as Error:
            msg = {"Error Message": Error}
            return msg
        

if __name__ == "__main__":
    NSXT_USERNAME = os.getenv("NSXT_USERNAME")
    NSXT_PASSWORD = os.getenv("NSXT_PASSWORD")
    BASE_URL = os.getenv("BASE_URL")
    DOMAIN_ID = os.getenv("DOMAIN_ID") 
    run = Get_All_Address_group(
                                NSXT_USERNAME, 
                                NSXT_PASSWORD, 
                                BASE_URL, 
                                DOMAIN_ID
                                )
    pprint(run.Address_groups())
