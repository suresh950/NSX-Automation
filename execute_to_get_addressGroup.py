import sys
import os
from dotenv import load_dotenv
load_dotenv()
from FilterAddressGroupFromRawData import FilterAddressGroupFromRawData
from get_All_Address_group import Get_All_Address_group
from pprint import pprint
NSXT_USERNAME = os.getenv("NSXT_USERNAME")
NSXT_PASSWORD = os.getenv("NSXT_PASSWORD")
BASE_URL = os.getenv("BASE_URL")
DOMAIN_ID = os.getenv("DOMAIN_ID") 
run = Get_All_Address_group(
                            NSXT_USERNAME, 
                            NSXT_PASSWORD, 
                            BASE_URL, 
                            DOMAIN_ID)

API_responce_raw_data = run.Address_groups()
test = FilterAddressGroupFromRawData(API_responce_raw_data)
pprint(test.get_address_group())
