from config import TwitterAuthenticate
from tweepy import API
from tweepy import Cursor
import json
import re
import pandas as pd
import numpy as np
from textblob import TextBlob

class TwitterClient():
    """
    Class retrieves tweets from a particular user and saves them to a json file
    """
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticate().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        # self.fetched_tweets_filename = fetched_tweets_filename
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

class TweetAnalyzer():
    '''
    Create pd data frame
    '''
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.id for tweet in tweets], columns=['id'])

        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['user'] = np.array([tweet.user.name for tweet in tweets])
        df['text'] = np.array([tweet.text for tweet in tweets])
        df['char_count'] = np.array([len(tweet.text) for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df

    def clean_text(self, text):
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

    def analyze_sentiment(self, text):
        analysis = TextBlob(self.clean_text(text))
        return analysis.sentiment.polarity

if __name__ == "__main__":
    user = "realDonaldTrump"
    tweet_analyzer = TweetAnalyzer()
    twitter_client = TwitterClient()
    api = twitter_client.get_twitter_client_api()

    desired_width = 320
    pd.set_option('display.width', desired_width)
    np.set_printoptions(linewidth=desired_width)
    pd.set_option('display.max_columns', 10)

    tweets = api.user_timeline(screen_name=user, count=100)

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(text) for text in df['text']])

    print(df)





    # Extract _json portion of tweepy Status object
    # json_str_list = []
    # for status in data:
    #     json_str = json.dumps(status._json)
    #     json_str_list.append(json_str)

    # print(json_str_list)
    # print(type(json_str_list))
    # with open(r"data/scratch.json", 'a') as f:
    #     for i in json_str_list:
    #         f.write(',[' + i + ']\n')







