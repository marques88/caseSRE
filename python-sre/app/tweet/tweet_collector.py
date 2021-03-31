from pymongo import MongoClient
from datetime import datetime
import tweepy
import sys
import re
import time
import os

#chaves privadas do twitter
CONSUMER_KEY = YOUR_CONSUMER_KEY
CONSUMER_SECRET = YOUR_CONSUMER_SECRET
ACCESS_TOKEN = YOUR_ACCESS_TOKEN
ACCESS_TOKEN_SECRET = YOUR_ACCESS_TOKEN_SECRET



class TweetCollector:
    def __init__(self):         
        self.__init_mongo_database()
        self.__init_twitter_api()

    def filter_by_id(self, obj):
        item_to_query = {"_id": obj["_id"]}        
        items = self.get_tweet_from_db_by_id(item_to_query)        
        return obj["_id"] not in items

    def get_tweets_from_db(self):
        tweets = self.database.tweets.find()
        novos_tweets = filter(self.filter_by_id, tweets)
        for tweet in novos_tweets:
            print(tweet)
        return list(tweets)

    def get_tweet_from_db_by_id(self, item_to_query):
        tweets_table = self.database.tweets
        items = tweets_table.find(item_to_query)
        ids = []        
        [ids.append(item["_id"]) for item in items]
        return ids

    def get_tweets_by_term_from_twitter(
        self, keyword, count=10, since=datetime(2021, 3, 1, 0, 0, 0)
    ):
        public_tweets = tweepy.Cursor(
            self.api.search,
            q=keyword,
            tweet_mode="extended",
            result_type="mixed",
            since=since.date(),
            include_entities=True,
        ).items(count)

        tweets = []
        # count_dir = 0
        for tweet in public_tweets:
            if not "retweeted_status" in dir(tweet):
                tweet_text = self.__clean_tweet(tweet.full_text)

                tweet_data = {
                    "_id": tweet.id,
                    "ScreenName": tweet.user.screen_name,
                    "UserName": tweet.user.name,
                    "UserLocation": tweet.user.location,
                    "Followers": tweet.user.followers_count,
                    "TweetText": tweet_text,
                    "Date": tweet.created_at,
                    "HashTags": self.__get_hashtags(tweet.entities["hashtags"]),
                }

                # if count_dir == 0:
                #     print(dir(tweet))
                #     count_dir = count_dir + 1

                tweets.append(tweet_data)

        return tweets

    def save_tweets_on_database(self, tweets=[]):

        for duplicated in tweets:
            tweet_id = duplicated["_id"]
            print(f"Procurando por {tweet_id}")
            tw = self.database.tweets.find({"_id": tweet_id})
            print(f"in database: {len(list(tw))}")
            count = tweets.count({"_id": tweet_id})
            print(f"in list {count}")


        novos_tweets = list(filter(self.filter_by_id, tweets))
        if len(novos_tweets) > 0:
            print(f"gravando {len(novos_tweets)} novos tweets")
            [print(tw_id["_id"]) for tw_id in novos_tweets]
            self.database.tweets.insert_many(novos_tweets)
        else:
            print("Não há novos tweets a inserir")

    def drop_table(self):
        self.database.tweets.drop()

    def summary(self):

        top_users = self.__get_top_five_user_with_most_followers()
        tweets_by_hour = self.__get_number_of_tweets_by_hour()
        tweets_by_location = self.__get_number_of_tweets_tags_by_location()

        result = {
            "top_users": top_users,
            "twets_by_hour": tweets_by_hour,
            "twets_by_location": tweets_by_location,
        }

        return result

    def __clean_tweet(self, tweets_text=""):

        clean_text = re.sub(r"RT+", "", tweets_text)
        clean_text = re.sub(r"@\S+", "", clean_text)
        clean_text = re.sub(r"https?\S+", "", clean_text)
        clean_text = clean_text.replace("\n", " ")

        return clean_text

    def __init_mongo_database(self):
        hostname = os.environ['MONGODB_HOSTNAME']
        mongo_user = os.environ['MONGODB_USERNAME']
        mongo_pwd = os.environ['MONGODB_PASSWORD']
        # database = 'tweets_python'    
        print(f"Initializing connection to mongo database in {hostname}")
        mongo_client = MongoClient(f'mongodb://{mongo_user}:{mongo_pwd}@{hostname}:27017/')
        self.database = mongo_client.tweets_python
        print(mongo_client.database_names())        

    def __init_twitter_api(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def __get_top_five_user_with_most_followers(self):
        tweets_table = self.database.tweets
        users_with_top_followers = tweets_table.find().sort("Followers", -1).limit(5)

        top_users = []
        for user in users_with_top_followers:
            tuser = user["ScreenName"]
            tfollowers = user["Followers"]
            top_users.append({"user": tuser, "num_followers": tfollowers})

        return top_users

    def __get_number_of_tweets_by_hour(self):
        tweets_table = self.database.tweets
        pipeline = [
            {"$group": {"_id": {"$hour": "$Date"}, "num_tweets": {"$sum": 1}}},
            {"$sort": {"num_tweets": -1}},
        ]
        agg_result = tweets_table.aggregate(pipeline)
        agregados = []
        for agregado in agg_result:
            agregados.append(
                {"hora": agregado["_id"], "num_tweets": agregado["num_tweets"]}
            )

        return agregados

    def __get_number_of_tweets_tags_by_location(self):
        tweets_table = self.database.tweets
        pipeline = [
            {"$unwind": "$HashTags"},
            {
                "$group": {
                    "_id": {"location": "$UserLocation", "hashtag": "$HashTags" },
                    "num_tweets": {"$sum": 1},
                }
            },
            {"$sort": {"num_tweets": -1}},
        ]

        aggregation_result = tweets_table.aggregate(pipeline)
        agregados = []
        [
            agregados.append(
                {"user_location": agregado["_id"], "num_tweets": agregado["num_tweets"]}
            )
            for agregado in aggregation_result
        ]

        return agregados

    def __get_hashtags(self, hashtags_entity):
        hashtags = []
        [hashtags.append(hashtag["text"]) for hashtag in hashtags_entity]

        return hashtags
