import re
import tweepy
from datetime import datetime
from textblob import TextBlob

CONSUMER_KEY = YOUR_CONSUMER_KEY
CONSUMER_SECRET = YOUR_CONSUMER_SECRET
ACCESS_TOKEN = YOUR_ACCESS_TOKEN
ACCESS_TOKEN_SECRET = YOUR_ACCESS_TOKEN_SECRET

keyword = ("'Black is King' OR 'black is king' OR 'Beyonce' OR 'beyonce' OR #blackisking OR '#BlackIsKing' OR 'black is king beyonce'")
count = 5000

class TweetAnalyzer():

  def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
    '''
      Conectar com o tweepy
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    self.con_token = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=5, retry_delay=10)

  def __clean_tweet(self, tweets_text):
    '''
    Tweet cleansing.
    '''

    clean_text = re.sub(r'RT+', '', tweets_text) 
    clean_text = re.sub(r'@\S+', '', clean_text)  
    clean_text = re.sub(r'https?\S+', '', clean_text) 
    clean_text = clean_text.replace("\n", " ")

    return clean_text

  def search_by_keyword(self, keyword, count=10, result_type='mixed', lang='en', tweet_mode='extended'):
    '''
      Search for the twitters thar has commented the keyword subject.
    '''
    tweets_iter = tweepy.Cursor(self.conToken.search,
                          q=keyword, tweet_mode=tweet_mode,
                          rpp=count, result_type=result_type,
                          since=datetime(2020,7,31,0,0,0).date(),
                          lang=lang, include_entities=True).items(count)

    return tweets_iter

  def prepare_tweets_list(self, tweets_iter):
    '''
      Transforming the data to DataFrame.
    '''

    tweets_data_list = []
    for tweet in tweets_iter:
      if not 'retweeted_status' in dir(tweet):
        tweet_text = self.__clean_tweet(tweet.full_text)
        tweets_data = {
            'len' : len(tweet_text),
            'ID' : tweet.id,
            'User' : tweet.user.screen_name,
            'UserName' : tweet.user.name,
            'UserLocation' : tweet.user.location,
            'TweetText' : tweet_text,
            'Language' : tweet.user.lang,
            'Date' : tweet.created_at,
            'Source': tweet.source,
            'Likes' : tweet.favorite_count,
            'Retweets' : tweet.retweet_count,
            'Coordinates' : tweet.coordinates,
            'Place' : tweet.place 
        }

        tweets_data_list.append(tweets_data)

    return tweets_data_list

  def sentiment_polarity(self, tweets_text_list):
      tweets_sentiments_list = []

      for tweet in tweets_text_list:
        polarity = TextBlob(tweet).sentiment.polarity
        if polarity > 0:
          tweets_sentiments_list.append('Positive')
        elif polarity < 0:
          tweets_sentiments_list.append('Negative')
        else:
          tweets_sentiments_list.append('Neutral')

      return tweets_sentiments_list

# Agora basta realizar as chamadas das classes para desfrutar das funções.
analyzer = TweetAnalyzer(consumer_key = CONSUMER_KEY, consumer_secret = CONSUMER_SECRET, 
access_token = ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

# Para realizar as buscas usando a keyword e quantidade predefinida e converter em uma lista.
tweets_iter = analyzer.search_by_keyword(keyword, count)
tweets_list = analyzer.prepare_tweets_list(tweets_iter)

# Uso de um Dataframe para melhor manipulação
tweets_df = pd.DataFrame(tweets_list)

# Chamar a função para análise de sentimentos
tweets_df['Sentiment'] = analyzer.sentiment_polarity(tweets_df['TweetText'])
