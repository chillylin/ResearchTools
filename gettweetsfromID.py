import pandas as pd
import tweepy 
import time
import pickle

key = {
  "consumer_key": ,# key
  "consumer_secret": , # secret
  "access_token": , # Token 
  "access_token_secret": # Token secret
}


#Twitter API credentials

consumer_key = key["consumer_key"]
consumer_secret = key["consumer_secret"]
access_key  = key["access_token"]
access_secret  = key["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def collect(id_list):
    batch_size = 100  # http://docs.tweepy.org/en/v3.5.0/api.html#API.statuses_lookup
    batch_indices = range(0, len(id_list), batch_size)
    batches = [id_list[i:i + batch_size] for i in batch_indices]
    
    tweetbatchlist = []
    
    for batch in batches:
        tweetbatchlist.append(api.statuses_lookup(batch, tweet_mode='extended'))
        time.sleep(1)  # don't hit API rate limit
        
    return tweetbatchlist

def dataframiseTweet(tweet):
    tempdict = {}

    tempdict['created_at'] = tweet['created_at']
    tempdict['tweetid'] = tweet['id']

    
    tempdict['text'] = tweet['full_text'] 
    tempdict['userId'] = tweet['user']['id']
    tempdict['userName'] = tweet['user']['name']
    tempdict['screen_name'] = tweet['user']['screen_name']

    tempdict['in_reply_to_status_id'] = tweet['in_reply_to_status_id']

    tempdict['mentioneeId'] = tweet['in_reply_to_user_id']
    tempdict['mentioneeScreenname'] = tweet['in_reply_to_screen_name']
    
    tempdict['RT'] = tweet['retweet_count']
    tempdict['Like'] = tweet['favorite_count']


    if len(tweet['entities']['user_mentions'])>0:

        tempdict['mentioneeName'] = tweet['entities']['user_mentions'][0]['name']

    return pd.DataFrame(tempdict, index  =[''])

# Collect tweets and save
idlist = [] # insert list of ID here
tweets = collect(idlist)
pickle.dump(tweets, open('tweets.pkl','wb')) 


# Read Twitter result and convert to dataframe 
dfs = []

count = 0
for resultset in tweets:
    for tweet in resultset:
        dfs.append(dataframiseTweet(tweet._json))
        count+=1

tweetdf = pd.concat(dfs)
tweetdf.to_pickle('TweetsDF.pkl')
