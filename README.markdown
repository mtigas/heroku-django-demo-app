This repo goes along with a **[how-to I've written for running Django on Heroku][howto]**.
You should probably check that out first.

A basic Django-on-Heroku example. Similar to what you get when you follow the
[Heroku Django starter doc][heroku_django], but with some extra bits:

* Runs on [gunicorn][gunicorn] with the [gevent worker class][gunicorn_design],
  to safely handle direct Web traffic.
* Uses `django-storages` and `boto` to store and serve static files
  and uploaded media in Amazon S3.
* Cache is enabled [as per the Heroku memcached docs][heroku_memcached].
* GzipMiddleware is enabled.
* Uses the [Heroku "piggyback" SSL addon][heroku_ssl] and
  [a Django middleware to enforce SSL][ssl_middleware].

An example of this demo (more or less) is running at
[https://tigas-test-app.herokuapp.com/](https://tigas-test-app.herokuapp.com/)
(with the adminsite disabled).

[howto]: http://mike.tig.as/blog/2012/02/13/deploying-django-on-heroku/
[heroku_django]: http://devcenter.heroku.com/articles/django
[gunicorn]: http://gunicorn.org/
[gunicorn_design]: http://gunicorn.org/design.html
[heroku_memcached]: http://devcenter.heroku.com/articles/memcache
[heroku_ssl]: http://devcenter.heroku.com/articles/ssl
[ssl_middleware]: https://gist.github.com/1812422
