import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    # load keys from csv file
    keys = loadkeys(twitter_auth_filename)
    # authorize consumer key and secret
    auth = tweepy.OAuthHandler(keys[0], keys[1])

    # set access to user access key and secret
    auth.set_access_token(keys[2], keys[3])

    # call api
    api = tweepy.API(auth)

    return api


def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """
    # Create a SentimentIntesityAnalyzer() object
    sid_object = SentimentIntensityAnalyzer()

    # extract tweets
    tweets = tweepy.Cursor(api.user_timeline, screen_name=name).items(100)
    
    tweets_list = []
    for tweet in tweets:
        cur = {}
        cur['id'] = tweet.id
        cur['created'] = tweet.created_at
        cur['retweeted'] = tweet.retweet_count
        cur['text'] = tweet.text
        cur['hashtags'] = tweet.entities['hashtags']
        cur['urls'] = tweet.entities['urls']
        cur['mentions'] = tweet.entities['user_mentions']
        sentiment_dict = sid_object.polarity_scores(cur['text'])
        cur['score'] = sentiment_dict['compound']
        tweets_list.append(cur)

    return {'user': name, 'count': len(tweets_list), 'tweets': tweets_list}


def fetch_following(api,name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get the list of User objects back from friends();
    get a maximum of 100 results. Pull the appropriate values from
    the User objects and put them into a dictionary for each friend.
    """
    # extract tweets
    friends = tweepy.Cursor(api.get_friends, screen_name=name).items(100)

    friends_list = []
    
    for friend in friends:
        cur = {}
        cur['name'] = friend.name
        cur['screen_name'] = friend.screen_name
        cur['followers'] = friend.followers_count
        cur['created'] = friend.created_at.date()
        cur['image'] = friend.profile_image_url

        friends_list.append(cur)

    # sort by follower count
    friends_list = sorted(friends_list, key=lambda friend: friend['followers'], reverse=True)

    return friends_list













