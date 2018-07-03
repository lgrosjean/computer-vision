from credentials import *
from tweepy import OAuthHandler, API


def api_init():
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret) 
	api = API(auth, wait_on_rate_limit=True)
	return api