import tweepy
import re
import config
import requests
import json

class KickzListener(tweepy.StreamListener):

    def notify_slack(self, link, image_link=None, desc=None):
        try:
            payload = { "text" : f"Product Link: <{link}>" }

            if image_link:
                payload['attachments'] = [
                    {
                        "title": desc,
                        "image_url": image_link
                    }
                ] 

            requests.post(config.SLACK_URL, data=json.dumps(payload))
        except Exception as e:
            print(f"Something went wrong:\n{e}")


    def on_status(self, tweet):
        try:
            urls = re.findall(config.LINK_REGEX, tweet.text)
            wonder = re.split(config.LINK_REGEX, tweet.text)
            if len(wonder) > 0:
                product_desc = wonder[0]

            product_link = next((url for index, url in enumerate(urls) if index == config.INDEX_OF_PRODUCT_LINK), config.NO_PRODUCT_LINK_FOUND)

            if product_link != config.NO_PRODUCT_LINK_FOUND and requests.get(product_link).status_code != 404:
                if 'media' in tweet.entities:
                    image_link = tweet.entities['media'][0]['media_url']
                    self.notify_slack(product_link, image_link, product_desc)
                else:
                    self.notify_slack(product_link, desc=product_desc)
                
                print(f"{tweet.text}\nProduct link: {product_link}\n{'*' * len(tweet.text)}")
        
        except Exception as e:
            print(f"Something went wrong:\n{e}")
        
        
        return True

    
    def on_error(self, status_code):
        print(f"Something went wrong:\n{status_code}")
        if status_code == 420:
            return False
        return True
