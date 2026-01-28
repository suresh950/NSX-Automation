'''
'''

class FilterAddressGroupFromRawDataV01():
    def __init__(self,rawData):
        self.rawData = rawData
    def get_parent_group_for_child_group(self,child_group):
        '''child_group is present in parent_group'''
        final_result = []
        for for_expression in self.rawData["results"]:
            if len(for_expression["expression"]) > 0:
                var_expression = for_expression["expression"]
                for item in var_expression:
                    if "paths" in item and len(item["paths"])>=1:
                        nested_member_group_list = {(newItem).split("/")[-1]: newItem  for newItem in item["paths"] }
                        if child_group in nested_member_group_list.keys():
                            result = {"display_name": for_expression["display_name"],"Nested_group_ID": for_expression["id"],"expression_id": item["id"],"Nested_member_path": nested_member_group_list[child_group]}
                            
                            final_result.append(result)

        return final_result
    '''=============================================================================================================='''
    def filter_TO_delete_Using_IP_list(self,ip_list):
        ''' This Returns list of dict for each group to be deleted, it checked only ip not nested group
        Creates final Entery in "Re_Create_Address_group": Re_Create_Address_group '''
        Re_Create_Address_group= []
        for item_in_results in self.rawData["results"]:
            display_name_of_item_in_results = item_in_results["display_name"]
            id_of_item_in_results = item_in_results["id"]
            if "description" in item_in_results:
                description= item_in_results["description"]
            else:
                description = "N/A"

            if len(item_in_results["expression"]) > 0:
                expression = item_in_results["expression"]
                for item_in_expression in expression:
                    if "paths" in item_in_expression:
                        break
                   
                    if "ip_addresses" in item_in_expression and len(item_in_expression["ip_addresses"]) >= 1 and set(item_in_expression["ip_addresses"]).issubset(ip_list):

                        payload = {
                            "resource_type": item_in_results["resource_type"],
                            "id": id_of_item_in_results,
                            "display_name": display_name_of_item_in_results,
                            "description": description,
                            "expression": [
                                {"resource_type": "IPAddressExpression", "ip_addresses": item_in_expression["ip_addresses"]}
                            ]
                        }
                        Re_Create_Address_group.append(payload)
        
        return Re_Create_Address_group
    '''=============================================================================================================='''
    # def filter_TO_update_Using_IP_list(self,ip_list):
    #     ''' This Returns list of dict for 
    #     '''
    #     IP_TO_Group= []
    #     for item_in_results in self.rawData["results"]:
    #         display_name_of_item_in_results = item_in_results["display_name"]
    #         id_of_item_in_results = item_in_results["id"]
    #         for item_in_expression in expression:
