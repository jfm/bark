import curses
import twitter
from bark.ui.bark_ui import BarkUI
from bark.config.config import BarkConfig
from bark.config.auth import PinAuthentication
from bark.config.consumer import BarkConsumer


class Bark:

    def main(self):
        bark_consumer = BarkConsumer()
        pin_auth = PinAuthentication()
        bark_config = BarkConfig(None)
        if bark_consumer.CONSUMER_KEY is None:
            CONSUMER_KEY = bark_config.get_value('API', 'consumer_key')
        else:
            CONSUMER_KEY = bark_consumer.CONSUMER_KEY

        if bark_consumer.CONSUMER_SECRET is None:
            CONSUMER_SECRET = bark_config.get_value('API', 'consumer_secret')
        else:
            CONSUMER_SECRET = bark_consumer.CONSUMER_SECRET

        if bark_config.get_value('API', 'access_token') is None:
            # TODO: Request access tokens with pin based auth
            pin_auth.get_access_token(CONSUMER_KEY, CONSUMER_SECRET)
            ACCESS_TOKEN = bark_config.get_value('API', 'access_token')
            ACCESS_TOKEN_SECRET = bark_config.get_value('API',
                                                        'access_token_secret')
        else:
            ACCESS_TOKEN = bark_config.get_value('API', 'access_token')
            ACCESS_TOKEN_SECRET = bark_config.get_value('API',
                                                        'access_token_secret')

        if CONSUMER_KEY is not None:
            api = twitter.Api(
                    consumer_key=CONSUMER_KEY,
                    consumer_secret=CONSUMER_SECRET,
                    access_token_key=ACCESS_TOKEN,
                    access_token_secret=ACCESS_TOKEN_SECRET,
                    tweet_mode='extended'
            )
            barkui = BarkUI(api)
            curses.wrapper(barkui.build_ui)
        else:
            print('Looks like you are running a git version.'
                  'Please get your consumer key and secret from Twitter'
                  'and add them to the configuration file')


if __name__ == '__main__':
    Bark().main()
