from pymongo import MongoClient
import json


def get_from_problems_db(number):
    client = MongoClient("mongodb://localhost:27017")
    db = client.zentaro
    res = db.problems.find_one({'number': number})
    return res


def get_dict_from_json(json_data):
    return json.loads(json_data)