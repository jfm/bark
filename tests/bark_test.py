import pytest
from pytest_mock import mocker
import twitter
from bark.ui.bark_curses import BarkCurses

class TestBarkCursesClass:

    def test_init_with_mock(self, mocker):
        mocker.patch.object(twitter, 'Api')
        bark = BarkCurses(twitter.Api())

    def test_validate_do_page_down(self, mocker):
        mocker.patch.object(twitter, 'Api')
        bark = BarkCurses(twitter.Api())
        mocker.patch.object(bark, 'do_page_down')
        bark.validate_input(338)
        bark.do_page_down.assert_called_with()

    def test_validate_do_page_up(self, mocker):
        mocker.patch.object(twitter, 'Api')
        bark = BarkCurses(twitter.Api())
        mocker.patch.object(bark, 'do_page_up')
        bark.validate_input(339)
        bark.do_page_up.assert_called_with()

    def test_handle_command_refresh(self, mocker):
        mocker.patch.object(twitter, 'Api')
        bark = BarkCurses(twitter.Api())
        mocker.patch.object(bark, 'do_refresh')
        bark.handle_command('/refresh')
        bark.do_refresh.assert_called_with()

    def test_handle_command_tweet(self, mocker):
        mocker.patch.object(twitter, 'Api')
        bark = BarkCurses(twitter.Api())
        mocker.patch.object(bark, 'do_tweet')
        bark.handle_command('/tweet tweeting message')
        bark.do_tweet.assert_called_with(['tweeting', 'message'])

    def test_handle_command_exit(self, mocker):
        mocker.patch.object(twitter, 'Api')
        bark = BarkCurses(twitter.Api())
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            bark.handle_command('/exit')
        assert pytest_wrapped_e.type == SystemExit
