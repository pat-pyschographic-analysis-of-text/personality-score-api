from ibm_watson import PersonalityInsightsV3
import tweepy
import json
import time
import os

IBM_API = 'https://gateway.watsonplatform.net/personality-insights/api'

TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

IBM_API_USERNAME = os.environ['IBM_API_USERNAME']
IBM_API_PASSWORD = os.environ['IBM_API_PASSWORD']

TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
TWITTER_AUTH.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

TWITTER = tweepy.API(TWITTER_AUTH)

def convert_status_to_pi_content_item(t,f):
    return {
        'content': t.full_text + f.text,
        'contenttype': 'text/plain',
        'created': int(time.mktime(t.created_at.timetuple())),
        'id': str(t.id),
        'language': t.lang
    }

def api(event, context):
    twitter_user = TWITTER.user_timeline(
        screen_name='austen',
        count=100,
        tweet_mode='extended'
    )

    favorites = TWITTER.favorites('austen',count=100)

    personality_insights = PersonalityInsightsV3(
        version='2017-10-13',
        url=IBM_API,
        iam_apikey=IBM_API_PASSWORD
    )
    
    pi_content_items_array = list(map(convert_status_to_pi_content_item, twitter_user, favorites))
    pi_content_items = {'contentItems': pi_content_items_array}
    data = json.dumps(pi_content_items, indent=2)
    
    profile = personality_insights.profile(
        data,
        accept='application/json',
        content_type='application/json',
        consumption_preferences=True,
        raw_scores=True
    ).get_result()
   
    return {
        'statusCode': 200,
        'body': profile
    }
