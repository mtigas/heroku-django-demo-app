from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from pprint import pformat
from datetime import datetime
import sys

@cache_page(60)
def home(request):
    txt = "<p><a href='/2/'>some pictures</a></p>"
    txt += "<p>time: %s (to test 60 second cache)</p>" % datetime.now()
    txt += "<pre>" + pformat(sys.path) + "</pre>"
    return HttpResponse(txt)
