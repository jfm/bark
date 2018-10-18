import curses
import pytest
from pytest_mock import mocker
import twitter
from bark.ui.bark_ui import BarkUI
from bark.ui.status_widget import StatusWidget

class TestBarkUIClass:

    def test_init_with_mock(self, mocker):
        mocker.patch.object(twitter, 'Api')
        bark = BarkUI(twitter.Api())

    def test_validate_do_page_down(self, mocker):
        mocker.patch.object(twitter, 'Api')
        bark = BarkUI(twitter.Api())
        mocker.patch.object(bark, 'do_page_down')
        bark.validate_input(338)
        bark.do_page_down.assert_called_with()

    def test_validate_do_page_up(self, mocker):
        mocker.patch.object(twitter, 'Api')
        bark = BarkUI(twitter.Api())
        mocker.patch.object(bark, 'do_page_up')
        bark.validate_input(339)
        bark.do_page_up.assert_called_with()

    def test_handle_command_tweet(self, mocker):
        mocker.patch.object(twitter, 'Api')
        bark = BarkUI(twitter.Api())
        mocker.patch.object(bark, 'do_tweet')
        bark.handle_command('/tweet tweeting message')
        bark.do_tweet.assert_called_with(['tweeting', 'message'])

    def test_do_tweet_too_long(self, mocker):
        curses.initscr()
        curses.start_color()
        mocker.patch.object(twitter, 'Api')
        api = twitter.Api()
        bark = BarkUI(api)
        bark.status_widget = StatusWidget(0,0)
        mocker.patch.object(bark.status_widget, 'set_status_text')
        bark.do_tweet("Message More than 240 characters long will cause us to set a status message which explains that the message was too long to be tweeted. Hopefully this will very rarely happen as people really should not write too long tweets. But we all know they will at some point.")
        bark.status_widget.set_status_text.assert_called()

    def test_do_heart(self, mocker):
        mocker.patch.object(twitter, 'Api')
        api = twitter.Api()
        bark = BarkUI(api)
        bark.tweets.append({'id': 'id1'})
        bark.tweets.append({'id': 'id2'})
        bark.do_heart('001')
        api.CreateFavorite.assert_called_with(status_id='id2')

    def test_do_retweet(self, mocker):
        mocker.patch.object(twitter, 'Api')
        api = twitter.Api()
        bark = BarkUI(api)
        bark.tweets.append({'id': 'id1'})
        bark.tweets.append({'id': 'id2'})
        bark.do_retweet('001')
        api.PostRetweet.assert_called_with('id2')


    def test_handle_command_exit(self, mocker):
        mocker.patch.object(twitter, 'Api')
        bark = BarkUI(twitter.Api())
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            bark.handle_command('/exit')
        assert pytest_wrapped_e.type == SystemExit
