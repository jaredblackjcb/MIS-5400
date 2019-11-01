from config import TwitterAuthenticate
from tweepy import API
from tweepy import Cursor
import json

class TwitterClient():
    """
    Class retrieves tweets from a particular user and saves them to a json file
    """
    def __init__(self, fetched_tweets_filename, twitter_user=None):
        self.auth = TwitterAuthenticate().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.fetched_tweets_filename = fetched_tweets_filename
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

if __name__ == "__main__":
    user = "realDonaldTrump"
    file_path = "data/scratch.json"

    client = TwitterClient(file_path, user)
    data = client.get_user_timeline_tweets(3)
    print(data)
    print(type(data))
    print(type(data[0]))


    # Extract _json portion of tweepy Status object
    json_str_list = []
    for status in data:
        json_str = json.dumps(status._json)
        json_str_list.append(json_str)

    print(json_str_list)





