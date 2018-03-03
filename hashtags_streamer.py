#!/usr/bin/env python

import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from pymongo import MongoClient
import os
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--mongo-host', help='MongoDB hostname or IP')
parser.add_argument('--mongo-port', help='MongoDB port')
args = parser.parse_args()

# MongoDB variables
mongo_host = args.mongo_host
mongo_port = int(args.mongo_port)
database = os.environ["database"]
collection = os.environ["collection"]

# MongoDB connection
client = MongoClient('mongodb://{}:{}/'.format(mongo_host, mongo_port))
db = client[database]


# Twitter authentication variables
consumer_key = os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']
access_token = os.environ['access_token']
access_secret = os.environ['access_secret']

# Twitter authentication
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# list of hashtags we are looking for
hashtags = os.environ['hashtags'].split()


class MyListener(StreamListener):

    def on_data(self, data):
        try:
            db[collection].insert_one(json.loads(data))
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


# stream tweets contained defined hashtags into MongoDB
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(
    track=hashtags
)
