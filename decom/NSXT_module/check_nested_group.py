import json
final_result = []
class CheckNestedGroup():
    def __init__(self, rawData):
        self.rawData = rawData
    
    def return_group_id_for_member_group_id(self, group_id):
        for for_expression in self.rawData["results"]:
            if len(for_expression["expression"]) > 0:
                var_expression = for_expression["expression"]
                for item in var_expression:
                    if "paths" in item:
                        nested_member_group_list = {(newItem).split("/")[-1]: newItem  for newItem in item["paths"] }
                        if group_id in nested_member_group_list.keys():
                            result = {"display_name": for_expression["display_name"],"Nested_group_ID": for_expression["id"],"expression_id": item["id"],"Nested_member_path": nested_member_group_list[group_id]}
                            
                            final_result.append(result)
        return final_result
