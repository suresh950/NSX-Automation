
class SecurityPolicyAndRules():
    def __init__(self,NSXT_session):
        self.NSXT_session = NSXT_session

    def list_all_policy(self,BASE_URL,DOMAIN_ID):
        '''Returns all the policy'''
        API_request = self.NSXT_session.get(f"{BASE_URL}/policy/api/v1/infra/domains/{DOMAIN_ID}/security-policies", 
                                            verify = False,
                                            timeout = 10)
        API_responce = API_request.json()
        return API_responce

    def list_all_rule(self,BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID):
        ''' Returns all the rules present in one policy'''
        API_request = self.NSXT_session.get(f"{BASE_URL}/policy/api/v1/infra/domains/{DOMAIN_ID}/security-policies/{SECURITY_POLICY_ID}/rules",
                                            verify = False,
                                            timeout = 10)

        API_responce = API_request.json()
        return API_responce
        
    def delete_rule(self,BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID,ROLE_ID):
        API_request = self.NSXT_session.delete(f"{BASE_URL}/policy/api/v1/infra/domains/{DOMAIN_ID}/security-policies/{SECURITY_POLICY_ID}/rules/{ROLE_ID}",
                                            verify = False,
                                            timeout = 10)
        return {"msg": API_request.status_code}

    def remove_group_from_src_and_dst(self,BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID,ROLE_ID,payload):
        '''Removes the Source group form the source list''' 
        API_request = self.NSXT_session.patch(f"{BASE_URL}/policy/api/v1/infra/domains/{DOMAIN_ID}/security-policies/{SECURITY_POLICY_ID}/rules/{ROLE_ID}",
                                            json = payload,
                                            verify = False,
                                            timeout = 10)
        '''# PATCH/PUT success responses often have no JSON body — never call .json() blindly'''
        return {"msg": API_request.status_code}
        # if API_request.status_code == 200:
        #     API_responce = API_request
        #     print(API_responce)
        #     # return API_responce
        '''
        This can be passed but check the code how i have passed data inFlight

        payload = {
                    "notes": rule["notes"],
                    "display_name": rule["display_name"],
                    "sequence_number": rule["sequence_number"],
                    "source_groups": rule["source_groups"],
                    "tag": rule["tag"],
                    "logged": rule["logged"],
                    "destination_groups": rule["destination_groups"],
                    "scope": rule["scope"] ,
                    "direction":rule["direction"], 
                    "action":  rule["action"] ,
                    "services": rule["services"],
                    "_revision": rule["_revision"]
                    }

        print(payload)
        '''

