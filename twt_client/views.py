from django.http import HttpResponse

# Create your views here.

def hello(request):
    html = "<html><body><h1>Hello</h1></body></html>"
    return HttpResponse(html)