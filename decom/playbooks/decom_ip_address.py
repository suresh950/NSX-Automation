"""
    Find the ip and remove it from every policy and address group
"""
import sys
import os
import json
import urllib3

import requests
import argparse
from datetime import datetime
from pytz import timezone
from pprint import pprint
from dotenv import load_dotenv
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from NSXT_module.Get_All_Address_group import Get_All_Address_group
from NSXT_module.Add_remove_addr_from_Addr_Group import Add_remove_addr_from_existing_group
from NSXT_module.FilterAddressGroupFromRawData import FilterAddressGroupFromRawData
from NSXT_module.FilterAddressGroupFromRawDataV01 import FilterAddressGroupFromRawDataV01
from NSXT_module.create_delete_group import CreateDeleteIpAddressGroup
from NSXT_module.add_remove_group_from_group import AddRemoveGroupFromGroup
from NSXT_module.security_policy_and_rules import SecurityPolicyAndRules

'''================================================================================================='''
load_dotenv()
tz = datetime.now().astimezone().tzinfo
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NSXT_USERNAME = os.getenv("NSXT_USERNAME")
NSXT_PASSWORD = os.getenv("NSXT_PASSWORD")
BASE_URL = os.getenv("BASE_URL")
DOMAIN_ID = os.getenv("DOMAIN_ID")

def decom_ip_address(ip_list):
    try:
        with requests.Session() as NSXT_session:
            '''==============================================================================================='''
            NSXT_session.auth = (NSXT_USERNAME, NSXT_PASSWORD) 
            '''================================================================================================'''

            '''================================================================================================'''
            # Decommission Action on the ip, if ip is added directly to rule without any Group 
            try:

                policys_for_individual_IP_check = SecurityPolicyAndRules(NSXT_session).list_all_policy(BASE_URL,DOMAIN_ID)
                policy_list = []
                for policy in policys_for_individual_IP_check["results"]:
                    policy_list.append({"id": policy["id"], "display_name": policy["display_name"], "category":policy["category"]})

                for policy_item in policy_list:
                    SECURITY_POLICY_ID = policy_item["id"]
                    POLICY_NAME = policy_item["display_name"]
                    CATEGORY = policy_item["category"]
                    rules = SecurityPolicyAndRules(NSXT_session).list_all_rule(BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID)
                
                    for rule in rules["results"]:
                        ROLE_ID = rule["id"]
                        display_name = rule["display_name"]
                        individual_source_IP_to_check = rule["source_groups"]
                        individual_destination_IP_to_check = rule["destination_groups"]
                        print(rule)
                        if set(individual_source_IP_to_check).issubset(ip_list):
                            delete_rule_with_individual_source_IP_responce = SecurityPolicyAndRules(NSXT_session).delete_rule(BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID,ROLE_ID)
                            print(f"{datetime.now()} ({tz}) CATEGORY: {CATEGORY}, POLICY_NAME: {POLICY_NAME}, Security Rule: {display_name} is deleted since it has only individual Source IP address, API Responce: {delete_rule_with_individual_source_IP_responce}")
                        elif set(individual_destination_IP_to_check).issubset(ip_list):
                            delete_rule_with_individual_source_IP_responce = SecurityPolicyAndRules(NSXT_session).delete_rule(BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID,ROLE_ID)
                            print(f"{datetime.now()} ({tz}) CATEGORY: {CATEGORY}, POLICY_NAME: {POLICY_NAME}, Security Rule: {display_name} is deleted since it has only individual Source IP address, API Responce: {delete_rule_with_individual_source_IP_responce}")
                        else:
                            for ip in  ip_list: 
                                if ip in individual_source_IP_to_check:
                                    rule["source_groups"].remove(ip)
                                    individual_source_IP_update_responce = SecurityPolicyAndRules(NSXT_session).remove_group_from_src_and_dst(BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID,ROLE_ID,rule)
                                    print(f"{datetime.now()} ({tz}) CATEGORY: {CATEGORY}, POLICY_NAME: {POLICY_NAME}, individual source IP {ip} has been removed from Security Rule: {display_name}")
                                
                                if ip in individual_destination_IP_to_check:
                                    rule["destination_groups"].remove(ip)
                                    individual_destination_IP_update_responce = SecurityPolicyAndRules(NSXT_session).remove_group_from_src_and_dst(BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID,ROLE_ID,rule)
                                    print(f"{datetime.now()} ({tz}) CATEGORY: {CATEGORY}, POLICY_NAME: {POLICY_NAME}, individual destination IP {ip} has been removed from Security Rule: {display_name}")
            except Exception as error: 
                print("Error Getting while <Decommission Action on the ip, if ip is added directly to rule without any Group>, Error:",error)
            '''================================================================================================'''
            try:
            # Update Security Policy (if source or destination has only group that is part of group to be deleted)
                policy_list = []
                policys = SecurityPolicyAndRules(NSXT_session).list_all_policy(BASE_URL,DOMAIN_ID)
                all_address_group_for_policys = Get_All_Address_group(NSXT_session).Address_groups()
                # print(policys["results"])
                for policy in policys["results"]:
                    policy_list.append({"id": policy["id"], "display_name": policy["display_name"], "category":policy["category"]})
                
                for for_expression in all_address_group_for_policys["results"]:

                    if len(for_expression["expression"]) > 0:
                        var_expression = for_expression["expression"]

                        for item in var_expression:
                            if "paths" in item:
                                break
                            if "ip_addresses" in item and len(item["ip_addresses"]) >= 1 and  set(item["ip_addresses"]).issubset(ip_list):
                                group_name = for_expression["display_name"]
                                group_id =  for_expression["id"]

                                for policy_item in policy_list:
                                    SECURITY_POLICY_ID = policy_item["id"]
                                    POLICY_NAME = policy_item["display_name"]
                                    CATEGORY = policy_item["category"]
                                    rules = SecurityPolicyAndRules(NSXT_session).list_all_rule(BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID)
                                    for rule in rules["results"]:
                                        source_groups_to_check = rule["source_groups"]
                                        destination_groups_to_check = rule["destination_groups"]
                                        
                                        ROLE_ID = rule["id"]

                                        # Source Address

                                        for src_check in source_groups_to_check:
                                            if src_check.split("/")[-1] == group_id and len(rule["source_groups"]) > 1:
                                                rule["source_groups"].remove(src_check)
                                                src_update_responce = SecurityPolicyAndRules(NSXT_session).remove_group_from_src_and_dst(BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID,ROLE_ID,rule)
                                                print(f"{datetime.now()} ({tz}) CATEGORY: {CATEGORY}, POLICY_NAME: {POLICY_NAME}, Source Address Group {group_id} has been removed from Security Rule: {ROLE_ID}")
                                            elif src_check.split("/")[-1] == group_id and len(rule["source_groups"]) == 1:
                                                delete_rule_responce = SecurityPolicyAndRules(NSXT_session).delete_rule(BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID,ROLE_ID)
                                                print(f"{datetime.now()} ({tz}) CATEGORY: {CATEGORY}, POLICY_NAME: {POLICY_NAME}, Security Rule: {ROLE_ID} is deleted since it has only one Source Group")
                                        
                                        # Destination Address

                                        for dst_check in destination_groups_to_check:
                                            if dst_check.split("/")[-1] == group_id and len(rule["destination_groups"]) > 1:
                                                rule["destination_groups"].remove(dst_check)
                                                src_update_responce = SecurityPolicyAndRules(NSXT_session).remove_group_from_src_and_dst(BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID,ROLE_ID,rule)
                                                print(f"{datetime.now()} ({tz}) CATEGORY: {CATEGORY}, POLICY_NAME: {POLICY_NAME}, Destination Address Group {group_id} has been removed from Security Rule: {ROLE_ID}")
                                            elif dst_check.split("/")[-1] == group_id and len(rule["destination_groups"]) == 1:
                                                delete_rule_responce = SecurityPolicyAndRules(NSXT_session).delete_rule(BASE_URL,DOMAIN_ID,SECURITY_POLICY_ID,ROLE_ID)
                                                print(f"{datetime.now()} ({tz}) CATEGORY: {CATEGORY}, POLICY_NAME: {POLICY_NAME}, Security Rule: {ROLE_ID} is deleted since it has only one Destination Group")

            except exceptions as error:
                print("Error Getting in section: <Update Security Policy (if source or destination has only group that is part of group to be deleted)>, Error: ",error)
            '''==========================================================================================================='''
            # Before deleting the group you need to remove from nested group if required
            try:
                all_address_group_for_nested_group = Get_All_Address_group(NSXT_session).Address_groups()
                for for_expression in all_address_group_for_nested_group["results"]:

                    if len(for_expression["expression"]) > 0:
                        var_expression = for_expression["expression"]
                        for item in var_expression:
                            if "paths" in item:
                                break
                            if "ip_addresses" in item and len(item["ip_addresses"]) >= 1 and  set(item["ip_addresses"]).issubset(ip_list):
                                parent_group_responce = FilterAddressGroupFromRawDataV01(all_address_group_for_nested_group).get_parent_group_for_child_group(for_expression['id'])
                                if len(parent_group_responce)>0:
                                    for payload_item in parent_group_responce:
                                        group_id = payload_item["Nested_group_ID"]
                                        expression_id = payload_item["expression_id"]
                                        payload = {"members": [payload_item["Nested_member_path"]]}
                                        responce = AddRemoveGroupFromGroup(NSXT_session).remove_member_grp(BASE_URL,DOMAIN_ID,group_id,expression_id,payload)
                                        
                                        if responce["msg"] == 200:
                                            print(f"{datetime.now()} ({tz}) Address Group member: {payload["members"][0].split("/")[-1]} removed from parent group: {payload_item["display_name"]}")
            except exceptions as error:
                print("Error Getting while <removing the nested group from the parent group>, Error:",error)
            '''============================================================================================================'''
            # # Section to Delete Address Group if there is no paths in var_expression
            try:
                all_address_group_for_deleting_group = Get_All_Address_group(NSXT_session).Address_groups()
                for for_expression in all_address_group_for_deleting_group["results"]:

                    if len(for_expression["expression"]) > 0:
                        var_expression = for_expression["expression"]
                        for item in var_expression:
                            if "paths" in item:
                                break
                            if "ip_addresses" in item and len(item["ip_addresses"]) >= 1 and  set(item["ip_addresses"]).issubset(ip_list):
                                
                                result_01 = CreateDeleteIpAddressGroup(NSXT_session).delete_IPaddress_group(BASE_URL, DOMAIN_ID, for_expression['id'])
                                
                                if result_01["msg"] == 200:
                                    print(f"{datetime.now()} ({tz}) Address Group: {for_expression['id']} is deleted")
            except exceptions as error:
                print("Error Getting in Section <to Delete Address Group>, Error:",error)
            '''=========================================================================================================='''
            # # To Remove individual IP address from other groups
            try: 
                all_address_group_to_Remove_individual_IP = Get_All_Address_group(NSXT_session).Address_groups()
                for ip_address in ip_list:

                    Total_Payload = FilterAddressGroupFromRawData(all_address_group_to_Remove_individual_IP).get_payload_For_single_IP(ip_address)

                    for single_payload in Total_Payload:
                        group_id = single_payload["group_id"]
                        ipaddressexp = single_payload["ipaddressexp"]
                        payload = {"ip_addresses": [ip_address]}

                        if ip_address in single_payload["payload"]["ip_addresses"]:

                            result = Add_remove_addr_from_existing_group(NSXT_session).remove_address(BASE_URL,DOMAIN_ID,group_id,ipaddressexp,payload)
                            if result["msg"] == 200:
                                print(f"{datetime.now()} ({tz}) IP address: {ip_address}, Removed from Address Group: {single_payload["Group_name_display_name"]}")
                            else:
                                print(f"{datetime.now()} ({tz}) IP address: {ip_address}, NOT Removed from Address Group: {single_payload["Group_name_display_name"]}. Please Try again.. OR May be this Group {single_payload["Group_name_display_name"]} is deleted please check the previous log")
            except exceptions as error:
                print("Error Getting in Section To <Remove individual IP address from other groups>, Error:",error)
            '''==================================================================================================================='''
    except Exception as Error:
        msg = {"Error":{Error}}
        print(msg)

ip_address_list = ["1.1.1.1","2.2.2.2","3.3.3.3","10.10.10.0/20"]
decom_ip_address(ip_address_list)
