
from elasticsearch import Elasticsearch
elastic = Elasticsearch()

# get the names of the indexes
# print ("\nPresent indices")
final_indices = elastic.indices.get_alias().keys()
# for _index in final_indices:
#     print ("Index name:", _index)


#----------------------------------- Delete an index ------------------------------------

# # iterate the list of indexes
# for _index in final_indices:
#     # attempt to delete ALL indices in a 'try' and 'catch block
#     try:
#         if "." not in _index: # avoid deleting indexes like `.kibana`
#             if _index == 'runnable':# delete only group index
#                 elastic.indices.delete(index=_index)
#                 print ("Successfully deleted:", _index)
#     except Exception as error:
#         print ('indices.delete error:', error, 'for index:', _index)


#----------------------------------- Create an index ------------------------------------
# now create a new index
# elastic.indices.create(index="new_index_name")
# elastic.index(index='groups', id=64, body = group_body)

# verify the new index was created
# final_indices = elastic.indices.get_alias().keys()
# print ("\nNew total:", len(final_indices), "indexes.")
# for _index in final_indices:
#     print ("Index name:", _index)


# print ("\nAll indices")
index = elastic.indices.get_alias().keys()
for _index in index:
    if "." not in _index:
        print ("\nIndex name:", _index + "\n")
        res = elastic.search(index = _index, size = 50)
        for doc in res['hits']['hits']:
            print(doc['_id'], doc['_source'])