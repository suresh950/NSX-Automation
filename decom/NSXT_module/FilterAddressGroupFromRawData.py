"""
    
"""
import json
from pprint import pprint

class FilterAddressGroupFromRawData():
    def __init__(self, rawData):
        self.rawData = rawData
        
    def get_address_group(self,):
        """
            This Returns all the Address Group and Address Object in a list of dictionary
        """ 
        group_data = []
        for each_group in self.rawData["results"]:
            if len(each_group["expression"]) > 0:
                expression = each_group["expression"][0]
                display_name = each_group["display_name"]
                if "ip_addresses" in expression:
                    temp = {}
                    temp["name"] = display_name
                    temp["value"] = expression["ip_addresses"]
                    group_data.append(temp)
                elif "paths" in expression:
                    temp2 = {}
                    group_list = [group.split("/")[-1] for group in expression["paths"]]
                    temp2["name"] = display_name
                    temp2["value"] = group_list
                    group_data.append(temp2)
        print("Data is Filterded")            
        return group_data

    def get_all_group_as_data_payload(self):
        """
            gets a payload that can be configured
        """
        get_raw_data_payload = []
        for for_expression in self.rawData["results"]:
            
            
            if len(for_expression["expression"]) > 0:
                    var_expression = for_expression["expression"]
                    for item in var_expression:
                        temp_data_for_payload_paths_group = {"group_id":"","ipaddressexp": "","payload": {"paths_group": []}}
                        temp_data_for_payload_ip_addresses = {"group_id":"","ipaddressexp": "","payload": {"ip_addresses": []}}
                        if "paths" in item:
                            temp_data_for_payload_paths_group["ipaddressexp"] = item["id"]
                            temp_data_for_payload_paths_group["group_id"] = for_expression["display_name"]
                            temp_data_for_payload_paths_group["payload"]["paths_group"] = [group.split("/")[-1] for group in item["paths"]]
                            get_raw_data_payload.append(temp_data_for_payload_paths_group)
                            
                        if "ip_addresses" in item:  
                            temp_data_for_payload_ip_addresses["ipaddressexp"] = item["id"]
                            temp_data_for_payload_ip_addresses["group_id"] = for_expression["display_name"]
                            temp_data_for_payload_ip_addresses["payload"]["ip_addresses"] = (item["ip_addresses"])
                            get_raw_data_payload.append(temp_data_for_payload_ip_addresses)
        
        return get_raw_data_payload
    
    def get_payload_For_single_IP(self,find_ipAddress):
        single_ip_payload_list =[]
        
        for for_expression in self.rawData["results"]:
            if len(for_expression["expression"]) > 0:
                var_expression = for_expression["expression"]
                for item in var_expression:
                    if "ip_addresses" in item:

                        temp_single_ip_payload = {"group_id":"","ipaddressexp": "","Group_name_display_name":"","payload": {"ip_addresses": []}}
                        if find_ipAddress in item["ip_addresses"]:
                            temp_single_ip_payload["ipaddressexp"] = item["id"]
                            temp_single_ip_payload["group_id"] = for_expression["id"]
                            temp_single_ip_payload["Group_name_display_name"] = for_expression["display_name"]
                            temp_single_ip_payload["payload"]["ip_addresses"] = item["ip_addresses"]
                            single_ip_payload_list.append(temp_single_ip_payload)


        return single_ip_payload_list

    def get_payload_For_single_member_group(self,member_group_name):
        single_member_group_payload_list =[]
        temp_single_member_group_payload = {"group_id":"","ipaddressexp": "","payload": {"paths_group": []}}
        for for_expression in self.rawData["results"]:
            if len(for_expression["expression"]) > 0:
                var_expression = for_expression["expression"]
                for item in var_expression:
                    if "paths" in item:
                        if member_group_name in [group.split("/")[-1] for group in item["paths"]]:
                            temp_single_member_group_payload["ipaddressexp"] = item["id"]
                            temp_single_member_group_payload["group_id"] = for_expression["display_name"]
                            temp_single_member_group_payload["payload"]["paths_group"] = member_group_name
                            single_member_group_payload_list.append(temp_single_member_group_payload)

        return single_member_group_payload_list

    def filter_to_delete_address_group_with_one_IP(self, ip):
        '''
            It has only ip that we have to decommission
        '''
        multi_payload = []
        for for_expression in self.rawData["results"]:
            
            if len(for_expression["expression"]) > 0:
                var_expression = for_expression["expression"]

                check_point = False
                for item in var_expression:
                    if "paths" in item:
                        check_point = True
                    if check_point:
                        continue
                        

                for item in var_expression:
                    if "ip_addresses" in item and len(item["ip_addresses"]) == 1 and item["ip_addresses"][0] == ip:

                        payload = {
                                "resource_type": for_expression["resource_type"],
                                "group_id": for_expression["id"],
                                "display_name": for_expression["display_name"],
                                "expression": [
                                    {"resource_type": "IPAddressExpression", "ip_addresses": item["ip_addresses"]}
                                ]
                            }
                        multi_payload.append(payload)
        return multi_payload

    def filter_to_delete_address_group_with_all_IP(self, ip_list):
        '''
            it Accept list of ip and checks if any group only IPs that are in ip_list
        '''
        multi_payload_new = []
        for for_expression in self.rawData["results"]:
            check_point = False
            if len(for_expression["expression"]) > 0:
                var_expression = for_expression["expression"]

                for item in var_expression:
                    if "paths" in item:
                        check_point = True
                if check_point:
                    continue
                    
                for item in var_expression:        
                    if "ip_addresses" in item and len(item["ip_addresses"]) >= 1 and set(item["ip_addresses"]).issubset(ip_list):

                        payload = {
                                "resource_type": for_expression["resource_type"],
                                "group_id": for_expression["id"],
                                "display_name": for_expression["display_name"],
                                "expression": [
                                    {"resource_type": "IPAddressExpression", "ip_addresses": item["ip_addresses"]}
                                ]
                            }
                        
                        multi_payload_new.append(payload)

        
        return multi_payload_new


