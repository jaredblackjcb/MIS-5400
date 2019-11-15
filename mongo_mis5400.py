import json
from pymongo import  MongoClient

if __name__ == "__main__":
    file = r"data/tweets.json"
    client = MongoClient('localhost', 27017)
    db = client['mis5400']
    trump_tweets = db['trump_tweets']

    with open(file, 'r') as f:
        data = json.load(f)

        db.insert_one(data)
