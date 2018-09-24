#!/bin/python
import pickle
import curses
import twitter
from twitter.models import Status
from bark.ui.bark_curses import BarkCurses
from bark.config.config import BarkConfig
from bark.config.auth import PinAuthentication
from bark.config.consumer import BarkConsumer

class Bark:
    def main(self):
        bark_consumer = BarkConsumer()
        pin_auth = PinAuthentication()
        bark_config = BarkConfig(None)
        if bark_consumer.CONSUMER_KEY == None:
            CONSUMER_KEY = bark_config.get_value('API', 'consumer_key')
        else:
            CONSUMER_KEY = bark_consumer.CONSUMER_KEY

        if bark_consumer.CONSUMER_SECRET == None:
            CONSUMER_SECRET = bark_config.get_value('API', 'consumer_secret')
        else:
            CONSUMER_SECRET = bark_consumer.CONSUMER_SECRET

        if bark_config.get_value('API', 'access_token') == None:
            #TODO: Request access tokens with pin based auth
            pin_auth.get_access_token(CONSUMER_KEY, CONSUMER_SECRET)
            ACCESS_TOKEN = bark_config.get_value('API', 'access_token')
            ACCESS_TOKEN_SECRET = bark_config.get_value('API', 'access_token_secret')
        else:
            ACCESS_TOKEN = bark_config.get_value('API', 'access_token')
            ACCESS_TOKEN_SECRET = bark_config.get_value('API', 'access_token_secret')

        api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)
        bark = BarkCurses(api)
        curses.wrapper(bark.main)

if __name__ == '__main__':
    Bark().main()
