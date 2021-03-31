from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from tweet.tweet_collector import TweetCollector
from datetime import datetime

tc = TweetCollector()
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return jsonify(hello="world")

@app.route("/tweets", methods=["GET"])
def home():
    tags = ["#openbanking", "#remediation", "#devops", "#sre", "#microservices", "#observability", "#oauth", "#metrics", "#logmonitoring", "#opentracing"]
    tweets = []
    for tag in tags:
        print(f"Buscando pela tag {tag}")
        tweets = tc.get_tweets_by_term_from_twitter(
            tag, 100, datetime(2021, 2, 26, 0, 0, 0)
        )
        tc.save_tweets_on_database(tweets)
    return jsonify(tweets), 200


@app.route("/tweets-summary", methods=["GET"])
def summary():
    return jsonify(tc.summary()), 200

@app.route("/tweets-from-db", methods=["GET"])
def tweets_from_db():
    return jsonify(tc.get_tweets_from_db()), 200

@app.route("/tweets", methods=["DELETE"])
def delete_tweets():
    tc.drop_table()
    return jsonify({"msg": "successfully deleted"}), 200

if __name__ == "__main__":
    print('executando main')
    app.run(debug=True)