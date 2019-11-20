from pymongo import MongoClient
from flask import Flask, g, render_template, abort, request
from bson.json_util import dumps
from bson.objectid import ObjectId


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
def get_all_books():
    client = MongoClient('localhost', 27017)
    db = client.twitter_data

    trump_tweets = db.trump_tweets.find()

    return dumps(trump_tweets), 200

# GET ONE /api/v1/trump_tweets
@app.route('/api/v1/trump_tweets/<string:id>', methods=['GET'])
def get_one_book():
    client = MongoClient('localhost', 27017)
    db = client.twitter_data
    # trump_tweets = db.trump_tweets

    book = db.trump_tweets.find({"_id": ObjectId(id)})

    return dumps(book), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
