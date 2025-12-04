"""
    data Cleaning
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



if __name__ == "__main__":
    path = "output_files/Group_list_03.json"
    run = FilterAddressGroupFromRawData(path)
    pprint(run.get_address_group())
