import tweepy
import config
import kickz_listener
import signal

def signal_handler(sig,frame):
    print("Exiting!")
    exit()
    my_stream.running = False

# Initial setup
auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
api = tweepy.API(auth)

signal.signal(signal.SIGINT, signal_handler)

# recent_tweets = api.user_timeline(config.USER_ID,count=4)
listener = kickz_listener.KickzListener()
""" for tweet in recent_tweets:
    listener.on_status(tweet) """
my_stream = tweepy.Stream(auth, listener) 

while not my_stream.running:
    try:
        print("[STREAM] Stream started!")
        my_stream.filter(follow=config.USER_IDS, _async=True)
    except Exception as ex:
        print ("[STREAM] Stream stopped! Reconnecting to twitter stream")
        print(ex)    
    

