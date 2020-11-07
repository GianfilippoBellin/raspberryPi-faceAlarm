from pymongo import MongoClient
import pymongo
import pprint
import datetime
import json

PATH_CONFIGURATIONS = "configurations/configurations.json"


class Connection:
    __URL = 'mongodb://face-alarm:ciao1994@vecchiagermania-shard-00-00.slhy8.mongodb.net:27017,vecchiagermania-shard-00-01.slhy8.mongodb.net:27017,vecchiagermania-shard-00-02.slhy8.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-10ovls-shard-0&authSource=admin&retryWrites=true&w=majority'

    __collection_connect = None
    name_database = 'face-alarm'
    id_camera = 1

    def connectMongoDB(self):
        client = MongoClient(self.__URL)
        # access to database
        return client.get_database(self.name_database)

    def getAll(self, have_to_show=False):
        collection = []
        # show all elements
        for a in self.__collection_connect.find():
            collection.append(a)
            if have_to_show:
                pprint.pprint(a)
        return collection

    def post(self, element, what_is):
        pass

    def get(self):
        pass

    def update(self, collection):
        pass

    def deleteAll(self):
        self.__collection_connect.delete_many({})


class FramesConnection(Connection):

    def __init__(self):
        self.__collection_connect = self.connectMongoDB().frames

    def post(self, frame, is_face):
        data = {
            "Frame": frame,
            "TimeStamp": datetime.datetime.utcnow(),
            "isFace": is_face,
            "CameraID": self.id_camera}
        res = self.__collection_connect.insert_one(data)


class ConfigurationsConnection(Connection):

    def __init__(self):
        self.__collection_connect = self.connectMongoDB().configurations

    def get(self):
        return self.__collection_connect.find_one({"id_cam": str(self.id_camera)})

    def saveConfigurations(self):
        data = self.get()
        del data['_id']
        file = open(PATH_CONFIGURATIONS, "w")
        json.dump(data, file)
        file.close()
