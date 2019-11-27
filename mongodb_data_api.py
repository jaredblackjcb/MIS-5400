from pymongo import MongoClient
from flask import Flask, g, render_template, abort, request
from bson.json_util import dumps
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client.twitter_data

# Setup Flask
app = Flask(__name__)
app.config.from_object(__name__)
@app.route('/')
def home_page():
    message = r"This is an api that exposes a MongoDB database containing Trump tweets." \
              r"All data can be accessed at the following address: /api/v1/trump_tweets"
    return message

# GET ALL /api/v1/trump_tweets
@app.route('/api/v1/trump_tweets', methods=['GET'])
def get_all_tweets():

    trump_tweets = db.trump_tweets.find()

    return dumps(trump_tweets), 200

# GET ONE /api/v1/trump_tweets
@app.route('/api/v1/trump_tweets/<string:id>', methods=['GET'])
def get_one_tweet(id):

    tweet = db.trump_tweets.find({"_id": int(id)})
    print(tweet)
    return dumps(tweet), 200

# POST API (Add)
@app.route('/api/v1/insert_tweet', methods=['POST'])
def insert_new():
    data = request.get_json()

    if isinstance(data, dict):
        db.trump_tweets.insert_one(data)

    if isinstance(data, list):
        db.trump_tweets.insert_many(data)

    return 'success', 200

# DELETE API
@app.route('/api/v1/delete/<string:id>', methods=['DELETE'])
def delete_one(id):
    db.trump_tweets.delete_one({'_id': int(id)})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
