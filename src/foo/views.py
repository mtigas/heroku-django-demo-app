from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from datetime import datetime
from foo.models import UserUploadedPhoto


@cache_page(60)
def two(request):
    txt = "<p><a href='/'>back to home</a></p>"
    txt += "<p>time: %s (to test 60 second cache)</p>" % datetime.now()
    for p in UserUploadedPhoto.objects.all().order_by('-id')[:5]:
        txt += "<p>%s<br><img style=\"max-width:300px\" src=\"%s\"></p>" % (p.name, p.photo.url)
    return HttpResponse(txt)
