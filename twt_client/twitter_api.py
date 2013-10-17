import yaml
from twython import Twython

def get_keys():
    with open("oauth.conf") as file:
        keys = yaml.load(file)

    print(keys)
    return keys

def list_timeline():
    keys = get_keys()

    twitter = Twython(keys['c_key'], keys['c_secret'], keys['a_token'],keys['a_secret'])
    print(twitter.get_home_timeline())


