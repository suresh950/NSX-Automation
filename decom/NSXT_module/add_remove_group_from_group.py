# New address can be created {and "_revision": number is used to update the existing the ip address and group}
import os
import sys
import json
import urllib3
import requests
from dotenv import load_dotenv

class AddRemoveGroupFromGroup():
    def __init__(self,NSXT_session):
        self.NSXT_session = NSXT_session

    def add_member_grp(self,BASE_URL,DOMAIN_ID,group_id,expression_id,payload):
        try:
            API_request = self.NSXT_session.post(f'{BASE_URL}/policy/api/v1/infra/domains/{DOMAIN_ID}/groups/{group_id}/path-expressions/{expression_id}?action=add', 
                                            json = payload,
                                            verify = False, 
                                            timeout = 10)

            API_responce = API_request.status_code
            return {"msg": API_responce}
        except Exception as Error:
            print(Error)

    def remove_member_grp(self,BASE_URL,DOMAIN_ID,group_id,expression_id,payload):
        try:
            API_request = self.NSXT_session.post(f'{BASE_URL}/policy/api/v1/infra/domains/{DOMAIN_ID}/groups/{group_id}/path-expressions/{expression_id}?action=remove', 
                                            json = payload,
                                            verify = False, 
                                            timeout = 10)

            API_responce = API_request.status_code
            return {"msg": API_responce}
        except Exception as Error:
            print(Error)


'''
  ==========================================================
    Here is how we can pass the variable to to the function
  ==========================================================
group_id = "GROUP_ID"
expression_id = "d77f7b00-4a1a-4ba7-acfb-d23a219e7020"
payload = {
            "members": ["/infra/domains/default/groups/putdecom_automate-grp-03-4"]
                    }
'''
