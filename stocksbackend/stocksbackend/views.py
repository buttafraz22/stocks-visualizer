from django.http import HttpResponse

# Create your views here.

def index_view(req):
    return HttpResponse('<h1>Hello World</h1>')