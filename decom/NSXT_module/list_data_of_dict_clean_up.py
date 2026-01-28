# Nested_group_cleanUP =  [
#         {
#             "display_name": "Nested-Group-1",
#             "group_id": "whout_address_and_group_member",
#             "expression_id": "93fae3a2-ce80-4ee9-9c1a-b86694e7c470",
#             "payload": {
#                 "members": [
#                     "/infra/domains/default/groups/Nested-member-1"
#                 ]
#             }
#         },
#         {
#             "display_name": "Nested-Group-2",
#             "group_id": "Nested-Group-2",
#             "expression_id": "940b36c8-7d13-4d44-b7fe-c61b16891204",
#             "payload": {
#                 "members": [
#                     "/infra/domains/default/groups/Nested-member-1"
#                 ]
#             }
#         },
#         {
#             "display_name": "Nested-Group-1",
#             "group_id": "whout_address_and_group_member",
#             "expression_id": "93fae3a2-ce80-4ee9-9c1a-b86694e7c470",
#             "payload": {
#                 "members": [
#                     "/infra/domains/default/groups/Nested-member-1"
#                 ]
#             }
#         },
#         {
#             "display_name": "Nested-Group-2",
#             "group_id": "Nested-Group-2",
#             "expression_id": "940b36c8-7d13-4d44-b7fe-c61b16891204",
#             "payload": {
#                 "members": [
#                     "/infra/domains/default/groups/Nested-member-1"
#                 ]
#             }
#         }
#     ]

class ListDataOfDictCleanUp():
    def __init__(self):
        pass

    def cleanUP(self, data):
        cleaned_data = []
        seen = set()
        for item in data:
            key = (
                item["display_name"],
                item["group_id"],
                item["expression_id"],
                tuple(item["payload"]["members"])
            )
            if key not in seen:
                seen.add(key)
                cleaned_data.append(item)

        return cleaned_data
