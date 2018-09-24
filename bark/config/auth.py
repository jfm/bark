from __future__ import print_function
from requests_oauthlib import OAuth1Session
from bark.config.config import BarkConfig
import webbrowser
import sys

class PinAuthentication:

    def __init__(self):
        self.REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
        self.ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
        self.AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
        self.SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'

        self.config = BarkConfig(None)

    def get_access_token(self, consumer_key, consumer_secret):
        oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri='oob')

        print('\nRequesting temp token from Twitter...\n')

        resp = oauth_client.fetch_request_token(self.REQUEST_TOKEN_URL)

        url = oauth_client.authorization_url(self.AUTHORIZATION_URL)

        print('I will try to start a browser to visit the following Twitter page '
                'if a browser will not start, copy the URL to your browser '
                'and retrieve the pincode to be used '
                'in the next step to obtaining an Authentication Token: \n'
                '\n\t{0}'.format(url))

        webbrowser.open(url)
        pincode = input('\nEnter your pincode? ')

        print('\nGenerating and signing request for an access token...\n')

        oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret,
                resource_owner_key=resp.get('oauth_token'),
                resource_owner_secret=resp.get('oauth_token_secret'),
                verifier=pincode)
        try:
            resp = oauth_client.fetch_access_token(self.ACCESS_TOKEN_URL)
        except ValueError as e:
            raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)

        self.config.set_value('API', 'access_token', resp.get('oauth_token'))
        self.config.set_value('API', 'access_token_secret', resp.get('oauth_token_secret'))
        print('''Your tokens/keys are as follows:
            access_token_key     = {atk}
            access_token_secret  = {ats}'''.format(
                atk=resp.get('oauth_token'),
                ats=resp.get('oauth_token_secret')))
