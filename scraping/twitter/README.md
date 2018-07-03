# Twitter Scraping

## Run scraping

``` 
> python  scraping_twitter.py -s THE_TEXT_TO_SEARCH -l NUMBER_OF_TWEET_TO_EXAMINATE
```

1. It will create a "photos" folder in the current directory if no one exists yet.
2. The folder will pop up to show the found pictures
3. A `.txt` file is created gathering information about the tweet in whoch the pictures have been found (creation date, username, text)

The scraping excludes pictures from retweeted tweets and searchs since the most recent tweets.

The API initialization is automatically done within the line 31 :
```
    api = api_init()
```

## Importing the code within another one

We can easly do this by putting : 
```
import scraping_twitter

scraping_twitter.tweet_scraping(THE_TEXT_TO_SEARCH, NUMBER_OF_TWEET_TO_EXAMINATE)
```