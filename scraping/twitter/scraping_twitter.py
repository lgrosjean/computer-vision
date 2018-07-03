import os
import tweepy
import json
import argparse
import time
from time import gmtime, strftime
import datetime
import wget
from api_setup import api_init
import urllib.request
import subprocess

def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    fromtime = datetime.datetime.fromtimestamp(now_timestamp)
    utcfromtime = datetime.datetime.utcfromtimestamp(now_timestamp)
    offset = fromtime - utcfromtime
    return utc_datetime + offset

def tweet_scraping(hashtag, length):

    CURRENT_FOLDER = os.getcwd()
    PHOTOS_PATH = os.path.join(CURRENT_FOLDER, "photos")

    # Starting time for information
    now_gm = gmtime()
    now = strftime("%Y%m%d-%H_%M_%S", now_gm)
    print(str(datetime.datetime.now()))

    # Twitter API initialization
    api = api_init()

    # Tweet scraping
    tweets = tweepy.Cursor(
        api.search, 
        q=hashtag + "-filter:retweets", 
         result_type="recent",
        include_rts=False,
        exclude_replies=True
        ).items(length)

    media_urls = list()

    i = 1

    if not os.path.exists(PHOTOS_PATH):
        os.makedirs(PHOTOS_PATH)

    INFO_NAME = now + "-" + hashtag + ".txt"
    INFO_PATH = os.path.join(PHOTOS_PATH, INFO_NAME)

    f = open(INFO_PATH, "w+")



    for tweet in tweets:

        if tweet.retweeted == False:

            # tweet.created_at, tweet.entities, tweet.text
            media = tweet.entities.get("media", None)

            if media != None:

                media = media[0]
                media_url = media.get("media_url", None)

                if media_url != None:

                    print(i, "pictures found!")

                    FILE_NAME = hashtag +str(i)+ ".jpg"    
                    FILE_PATH = os.path.join(PHOTOS_PATH, FILE_NAME)
                    
                    urllib.request.urlretrieve(media_url, FILE_PATH)

                    f.write(FILE_NAME)
                    f.write("\n")
                    f.write(str(tweet.user.screen_name))
                    f.write("\n")
                    f.write(str(datetime_from_utc_to_local(tweet.created_at)))
                    f.write("\n")
                    tweet_text = tweet.text.encode("utf-8")
                    f.write(str(tweet_text))
                    f.write("\n \n")

                    i += 1

    print("{} photos saved in {}".format(i-1, PHOTOS_PATH))

    popup_folder_cmd = 'explorer ' + PHOTOS_PATH
    subprocess.Popen(popup_folder_cmd)


if __name__ == '__main__':

    # Parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--search", required=True,
        help="Hashtag to search on twitter")
    ap.add_argument("-l", "--length", required=True,
        help="Number of tweets to scrap")

    args = vars(ap.parse_args())

    hashtag = args["search"]
    length = int(args["length"])

    tweet_scraping(hashtag, length)