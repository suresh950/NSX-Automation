import os
import sys
import json
import urllib3
import requests
from dotenv import load_dotenv
load_dotenv()

class Add_remove_addr_from_existing_group():
    def __init__(self,NSXT_session):
        self.NSXT_session = NSXT_session

    def add_address(self,BASE_URL,DOMAIN_ID,group_id,ipaddressexp,payload):
        '''
            Payload for both add and remove the address (if the ip address ("ip_addresses") is already present in it ). 

            group_id = "putdecom_automate-grp-5" this is id not display_name
            ipaddressexp = "8d00a238-d628-43da-9b2f-95f920fc982d"

            payload = {
                        "ip_addresses": [
                                    "10.110.9.4-10.110.9.10",
                                    "10.110.9.3/24"
                                ]
                        }
        '''
        try:
            API_request = self.NSXT_session.post(f'{BASE_URL}/policy/api/v1/infra/domains/{DOMAIN_ID}/groups/{group_id}/ip-address-expressions/{ipaddressexp}?action=add', 
                                            json = payload,
                                            verify = False, 
                                            timeout = 10)

            API_responce = API_request.status_code
            return {"msg": API_responce}
        except Exception as Error:
            print(Error)

    def remove_address(self,BASE_URL,DOMAIN_ID,group_id,ipaddressexp,payload):
        '''
            Payload for both add and remove the address (if the ip address ("ip_addresses") is already present in it ). 

            group_id = "putdecom_automate-grp-5" this is id not display_name
            ipaddressexp = "8d00a238-d628-43da-9b2f-95f920fc982d"

            payload = {
                        "ip_addresses": [
                                    "10.110.9.4-10.110.9.10",
                                    "10.110.9.3/24"
                                ]
                        }
            '''
        try:
            API_request = self.NSXT_session.post(f'{BASE_URL}/policy/api/v1/infra/domains/{DOMAIN_ID}/groups/{group_id}/ip-address-expressions/{ipaddressexp}?action=remove', 
                                            json = payload,
                                            verify = False, 
                                            timeout = 10)

            API_responce = API_request.status_code
            return {"msg": API_responce}
        except Exception as Error:
            print(Error)
    
    def additon_in_existing_addr_grp(self,BASE_URL,DOMAIN_ID,group_id,payload):
        '''
        This will replace the existing data you need to updend in existing then add or remove
        payload = {
                    "resource_type": "Group",
                    "id": "group-3",
                    "display_name": "group-3",
                    "_revision": 7,
                    "expression": [
                        {
                        "resource_type": "PathExpression",
                        "paths": [
                            "/infra/domains/default/groups/group-1",
                            "/infra/domains/default/groups/group-2"
                        ]
                        },
                        {
                        "resource_type": "ConjunctionOperator",
                        "conjunction_operator": "OR"
                        },
                        {
                        "resource_type": "IPAddressExpression",
                        "ip_addresses": [
                            "10.10.10.10",
                            "10.10.10.0/24"
                        ]
                        }
                    ]
                    }
        '''
        
        try:
            API_request = self.NSXT_session.put(f'{BASE_URL}/policy/api/v1/infra/domains/{DOMAIN_ID}/groups/{group_id}', 
                                            json = payload,
                                            verify = False, 
                                            timeout = 10)
                                                
            API_responce = API_request.status_code
            return {"msg": API_responce}
        except Exception as Error:
            print(Error)



# =============== Comment and notes below for this module ====================== 

# New address can be created {and "_revision": number is used to update the existing the ip address and group}

