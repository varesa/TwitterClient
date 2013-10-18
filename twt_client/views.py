from django.http import HttpResponse
from django.shortcuts import render_to_response

from twt_client.twitter_api import list_timeline

import pprint

pp = pprint.PrettyPrinter(indent=4)

# Create your views here.

def hello(request):
    html = "<html><body><h1>Hello</h1></body></html>"
    return HttpResponse(html)

def list_tweets(request):
    tweets = list_timeline()
    pp.pprint(tweets[0])
    return render_to_response('tweets.html', {'tweets':tweets})
    """html = "<html><body><h1>Test</h1></body></html>"
    return HttpResponse(html)"""