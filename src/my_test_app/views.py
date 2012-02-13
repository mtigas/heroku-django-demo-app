from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from pprint import pformat
from datetime import datetime
import sys

@cache_page(60)
def home(request):
    txt = "<p>(<b>This is a demo of running a basic Django site on Heroku:</b> <a href=\"http://mike.tig.as/blog/2012/02/13/deploying-django-on-heroku/\">See the tutorial post</a> or <a href=\"https://github.com/mtigas/heroku-django-demo-app\">the project source code.)</p>"
    txt += "<p><a href='/2/'>ImageField test here</a></p>"
    txt += "<p>time: %s (to test 60 second cache)</p>" % datetime.now()
    txt += "<pre>sys.path:\n" + pformat(sys.path) + "</pre>"
    return HttpResponse(txt)
