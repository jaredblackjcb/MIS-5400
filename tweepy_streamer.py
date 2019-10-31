from tweepy import API
from tweepy import Cursor
from tweepy import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pymongo
import json
import twitter_credentials
"""
Data not saving correctly from cursor. Only works with live streamer.
Data information:
I am retreiving Donald Trump's tweets and then doing a sentiment analysis on them and comparing them to moves in the S&P 500.
Data fields available include time, location, and text of tweet, number of retweets, number of likes, comments.
I can use many of those as variables to explain stock price fluctuations.
"""

class TwitterClient():
    """
    Class retrieves tweets from a particular user and saves them to a json file
    """
    def __init__(self, fetched_tweets_filename, twitter_user=None):
        self.auth = TwitterAuthenticate().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user
        self.fetched_tweets_filename = fetched_tweets_filename

    def get_user_timeline_tweets(self, num_tweets):
        #tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            #tweets.append(tweet)
            try:
                with open(self.fetched_tweets_filename, 'a') as tf:
                    tf.write(str(tweet))
            except Exception as e:
                print(f"Error retreiving data: {str(e)}")
        #return tweets

class TwitterAuthenticate():
    """
    Class contains logic for twitter API authentication and returns it as an object named "auth"
    """
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authentication = TwitterAuthenticate()

    def stream_tweets(self, fetched_tweets_filename, hashtag_list):
        # Handles authentication
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authentication.authenticate_twitter_app()
        stream = Stream(auth, listener)
        stream.filter(track=hashtag_list)

class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, raw_data):
        try:
            print(raw_data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(raw_data)
        except Exception as e:
            print(f"Error retreiving data: {str(e)}")


    def on_error(self, status_code):
        # Prevent throttling
        if status_code == 420:
            return False
        print(status_code)

if __name__ == "__main__":

    hashtag_list = ["trump", "china"]
    fetched_tweets_filename = "data/tweets.json"

    twitter_client = TwitterClient("data/tweets.json", "realDonaldTrump")
    twitter_client.get_user_timeline_tweets(1)
    #with open(f"data/tweets.json", 'w') as file:
     #   json.dump(data, file)



    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename, hashtag_list)

    #stream.firehose()
