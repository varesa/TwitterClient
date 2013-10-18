import json
import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils import timezone

from twt_client.models import Tweet, Meta
from twt_client.twitter_api import list_timeline

import pprint

pp = pprint.PrettyPrinter(indent=4)

# Create your views here.

def hello(request):
    html = "<html><body><h1>Hello</h1></body></html>"
    return HttpResponse(html)

def update(request=None):
    latest_id = Tweet.objects.latest('id')

    tweets = list_timeline(count = 400, since_id=latest_id)

    for tweet in tweets:
        Tweet(id = tweet['id'], data = json.dumps(tweet)).save()

    if len(tweets) == 400: # Get another set
        return update(request)

    newtime = Meta.objects.get(id=0)
    newtime.time = datetime.datetime.now().timestamp()
    newtime.save()

    if request is not None:
        return HttpResponse("<html><head></head><body>success</body></html>")

def update_if_necessary():
    try:
        expiretime = int(Meta.objects.get(id=0).time) + 300
    except Meta.DoesNotExist:
        Meta(id=0, time=datetime.datetime.now().timestamp()).save()

    now = datetime.datetime.now().timestamp()

    print("Expiration: " + str(expiretime))
    print("Now:        " + str(now))

    if now > expiretime:
        print("Not cached")
        update()

        newtime = Meta.objects.get(id=0)
        newtime.time = datetime.datetime.now().timestamp()
        newtime.save()
    else:
        print("Cached")

def list_tweets(request):
    update_if_necessary()

    tweets = []
    for tweet in sorted(Tweet.objects.all(), key=lambda tweet: datetime.datetime.strptime(json.loads(tweet.data)['created_at'], "%a %b %d %H:%M:%S %z %Y").timestamp(), reverse=False):
        data = json.loads(tweet.data)

        time = datetime.datetime.strptime(json.loads(tweet.data)['created_at'], "%a %b %d %H:%M:%S %z %Y").timestamp()
        if time > timezone.now().timestamp() - 60*60*24:
            if time > timezone.now().timestamp() - 60*60:
                minutes  = (timezone.now() - datetime.datetime.strptime(json.loads(tweet.data)['created_at'], "%a %b %d %H:%M:%S %z %Y")).seconds/60
                pretty = str(round(minutes)) + "m ago"
            else:
                hours  = (timezone.now() - datetime.datetime.strptime(json.loads(tweet.data)['created_at'], "%a %b %d %H:%M:%S %z %Y")).seconds/3600
                pretty = str(round(hours))+ "h ago"
        else:
            pretty = datetime.datetime.strptime(json.loads(tweet.data)['created_at'], "%a %b %d %H:%M:%S %z %Y").strftime("%d.%m %H:%M")

        data['pretty_time'] = pretty
        tweets.append(data)

    return render_to_response('tweets.html', {'tweets':tweets})