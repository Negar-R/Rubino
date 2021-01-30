from bson import ObjectId
from pymongo import MongoClient
from bson.json_util import dumps, loads
from LikeInstaProject.settings import MONGO_URI, MONGO_NAME
from instagram.models import Post, Profile


class MongoClientClass:
    def __init__(self, mongo_uri):
        self.mongo_client = MongoClient(mongo_uri, authSource="admin")
        self.mongo_db = self.mongo_client[MONGO_NAME]
        self.mongo_collection = ""

    def fetch_one_data(self, dbcollection: str, query: str, query_param):
        self.mongo_collection = self.mongo_db[dbcollection]
        data = self.mongo_collection.find_one({query: query_param})
        if data:
            if dbcollection == 'posts':
                data = Post(**data)
            elif dbcollection == 'profiles':
                data = Profile(**data)
        return data

    def fetch_data(self, dbcollection: str, query: str, query_param):
        self.mongo_collection = self.mongo_db[dbcollection]
        data = dumps(list(self.mongo_collection.find({query: query_param})))
        return loads(data)

    def insert_one_data(self, dbcollection: str, **kwargs):
        self.mongo_collection = self.mongo_db[dbcollection]
        data = self.mongo_collection.insert_one(kwargs)
        return data

    def delete_one_data(self, dbcollection: str, **kwargs):
        self.mongo_collection = self.mongo_db[dbcollection]
        self.mongo_collection.delete_one(kwargs)

    def update_data(self, dbcollection: str, filter_query, update_query, upsert):
        self.mongo_collection = self.mongo_db[dbcollection]
        data = self.mongo_collection.update_one(filter_query,
                                                update_query,
                                                upsert=upsert)
        return data

    def update_one_profile(self, dbcollection: str, query: str, query_param, **kwargs):
        username = kwargs.get('username')
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        picture = kwargs.get('picture')

        print(username, picture)
        self.mongo_collection = self.mongo_db[dbcollection]
        data = self.mongo_collection.find_one_and_update({query: query_param},
                                                         {"$set": {
                                                            'username': username,
                                                            'first_name': first_name,
                                                            'last_name': last_name,
                                                            'picture': picture
                                                         }},
                                                         upsert=False)
        if data:
            if dbcollection == 'posts':
                data = Post(**data)
            elif dbcollection == 'profiles':
                data = Profile(**data)
        return data

    def update_first_page(self, dbcollection: str, query: str, query_param, post_id: ObjectId):
        self.mongo_collection = self.mongo_db[dbcollection]
        data = self.mongo_collection.update_one({query: query_param},
                                                {"$push": {"inclusive_pots": post_id}},
                                                upsert=True)


mongo_client_obj = MongoClientClass(MONGO_URI)
