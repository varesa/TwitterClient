from django.http import HttpResponse

from twt_client.twitter_api import list_timeline

# Create your views here.

def hello(request):
    html = "<html><body><h1>Hello</h1></body></html>"
    return HttpResponse(html)

def list_tweets(request):
    list_timeline()
    html = "<html><body><h1>Test</h1></body></html>"
    return HttpResponse(html)