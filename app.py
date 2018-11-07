import tweepy
import config
import kickz_listener


# Initial setup
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
api = tweepy.API(auth)


# recent_tweets = api.user_timeline(config.USER_ID,count=4)
listener = kickz_listener.KickzListener()
""" for tweet in recent_tweets:
    listener.on_status(tweet) """
my_stream = tweepy.Stream(auth, listener) 


while not my_stream.running:
    try:
        print("[STREAM] Stream started!")
        my_stream.filter(follow=config.USER_IDS, _async=False)
    except KeyboardInterrupt as ex:
        print ("[STREAM] Stream stopped!")
        my_stream.running = False
        exit()
    except Exception as ex_dont_matter:
        my_stream.running = False
        print ("[STREAM] Stream stopped! Reconnecting to twitter stream")

        
    

