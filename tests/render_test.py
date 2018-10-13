import pickle
from bark.ui.rendering import Render

test_statuses = pickle.load( open("tests/status_dump.bin", "rb"))

def test_break_up_text():
    render = Render()
    text = test_statuses[0].text
    lines = render._break_up_text(text, 20)
    assert len(lines) == 8

def test_get_longest_username():
    render = Render()
    usernames = ['12345', '123456', '23456']
    length = render.get_longest_username(usernames)
    assert length == 6

def test_render_text():
    render = Render()
    text = test_statuses[0].text
    lines = render.render_text(text, 20)
    assert len(lines) == 8

def test_render_text_oneline():
    render = Render()
    text = "Hello World"
    lines = render.render_text(text, 20)
    assert len(lines) == 1

def test_render_text_on_length():
    render = Render()
    text = "123456789 123456 890"
    lines = render.render_text(text, 20)
    assert len(lines) == 2

def test_render_username():
    render = Render()
    username = render.render_username('MyUsername')
    assert username == 'MyUsername'

def test_render_time():
    render = Render()
    time = render.render_time(test_statuses[0].created_at)
    assert time == '08:03:11'

def test_render_tweet():
    render = Render()
    tweet = render.render_tweet(test_statuses[0], 20)
    assert tweet['time'] == '08:03:11'
    assert tweet['username'] == 'rustyshelf'
    assert len(tweet['tweet_lines']) == 8
