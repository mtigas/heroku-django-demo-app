from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from datetime import datetime
from foo.models import UserUploadedPhoto


@cache_page(60)
def two(request):
    txt = "<p>(<b>This is a demo of running a basic Django site on Heroku:</b> <a href=\"http://mike.tig.as/blog/2012/02/13/deploying-django-on-heroku/\">See the tutorial post</a> or <a href=\"https://github.com/mtigas/heroku-django-demo-app\">the project source code.)</p>"
    txt += "<p><a href='/'>back to home</a></p>"
    txt += "<p>time: %s (to test 60 second cache)</p>" % datetime.now()
    for p in UserUploadedPhoto.objects.all().order_by('-id')[:5]:
        txt += "<p>%s<br><img style=\"max-width:300px\" src=\"%s\"></p>" % (p.name, p.photo.url)
    return HttpResponse(txt)
