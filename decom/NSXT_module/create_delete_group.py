import os
import sys
import json
import urllib3
import requests
from dotenv import load_dotenv
load_dotenv()

class CreateDeleteIpAddressGroup():
    def __init__(self,NSXT_session):
        self.NSXT_session = NSXT_session
    
    def create_IPaddress_group(self,BASE_URL,DOMAIN_ID,group_id,payload):
        url = f"{BASE_URL}/policy/api/v1/infra/domains/{DOMAIN_ID}/groups/{group_id}"
        api_response = self.NSXT_session.put(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            verify=False,
            timeout=30
        )
        return {"msg": api_response.status_code} 

    def delete_IPaddress_group(self, BASE_URL, DOMAIN_ID, group_id):
        ''' Only it needs a Group_id to delete the group'''
        url = f"{BASE_URL}/policy/api/v1/infra/domains/{DOMAIN_ID}/groups/{group_id}"

        api_response = self.NSXT_session.delete(
            url,
            verify=False,
            timeout=30
        )

        return {"msg": api_response.status_code}  

# =================To create only New group========================     
# The Payload is to create new IP address Group                                 
'''
        payload = {
            "resource_type": "Group",
            "id": f"{group_id}",
            "display_name": "GROUP_ID",
            "description": "Created New Group using python",
            "expression": [
                {"resource_type": "IPAddressExpression", "ip_addresses": IP_ADDRESSES}
            ]
        }

'''

# To Delete the Group you just need to provide the group_id 
"""
    group_id
"""
