import tweepy, ibm_watson
import json, time, os

IBM_API = 'https://gateway.watsonplatform.net/personality-insights/api'

TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

IBM_API_USERNAME = os.environ['IBM_API_USERNAME']
IBM_API_PASSWORD = os.environ['IBM_API_PASSWORD']

TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
TWITTER_AUTH.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)

TWITTER = tweepy.API(TWITTER_AUTH)

DEFAULT_USERNAME = 'austen'

def format_for_ibm_api(t,f):
    return {
        'content': t.full_text + f.text,
        'contenttype': 'text/plain',
        'created': int(time.mktime(t.created_at.timetuple())),
        'id': str(t.id),
        'language': t.lang
    }

def twitter_to_personality_scores(timeline, favorites):
    insights = ibm_watson.PersonalityInsightsV3(version='2017-10-13', url=IBM_API, iam_apikey=IBM_API_PASSWORD)

    ibm_formatted_tweets = list(map(format_for_ibm_api, timeline, favorites))
    tweets = json.dumps({ 'contentItems': ibm_formatted_tweets }, indent=2)

    scores = insights.profile(
        tweets,
        accept='application/json',
        content_type='application/json',
        consumption_preferences=True,
        raw_scores=True
    )

    return scores.get_result()

def main(event, context):
    body = json.loads(event.get('body', "{}"))
    username = body.get('username', DEFAULT_USERNAME)

    timeline = TWITTER.user_timeline(screen_name=username, count=100, tweet_mode='extended')
    favorites = TWITTER.favorites(username, count=100)

    body = json.dumps(twitter_to_personality_scores(timeline, favorites))

    return { 'statusCode': 200, 'body': body }
