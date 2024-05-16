"""
create account
network access 0.0.0.0/
"""
import pymongo

uri = "mongodb+srv://damanpreet01:abc@cluster0.crerpeh.mongodb.net/?retryWrites=true&w=majiority"
client = pymongo.MongoClient(uri)
db = client['majorproject']
collections = db.list_collection_names()
# print(collections)
for collection in collections:
    print(collection)
#documents = db['patients'].find()
#for document in documents:
 #   print(document)
#documents = db['consultations'].find()
#for document in documents:
 #   print(document)

