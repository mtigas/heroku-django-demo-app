The **tldr** of **[this how-to blogpost][howto]**.

[howto]: http://mike.tig.as/blog/2012/02/12/deploying-django-on-heroku/

You should be running on Mac OS X and have the following packages:

* git
* python 2.7.x
* pip
* virtualenv
* heroku
* foreman

If not, read the ***Preliminaries*** section of that blogpost before continuing.


### Bootstrapping a Django-on-Heroku app

    # The "app name" that this will get in the Heroku control panel. Also
    # determines directory names and your "PROJECT_NAME.herokuapp.com"
    # default domain.
    export PROJECT_NAME="my-test-app"

    # The python module name for your Django site. Separate from above since
    # python app names should use underscores rather than dashes.
    export PYTHON_APP_NAME="my_test_app"

    # Set up a heroku-$PROJECT_NAME virtualenv in the ~/Code directory.
    cd ~/Code
    virtualenv --no-site-packages heroku-$PROJECT_NAME

    # Modify the `activate` file with some sanity-ensuring defaults, like
    # ignoring any system-level PYTHONPATH and DJANGO_SETTINGS_MODULE.
    cd heroku-$PROJECT_NAME
    echo "export PROJECT_NAME=\"$PROJECT_NAME\"" >> bin/activate
    echo "export PYTHON_APP_NAME=\"$PYTHON_APP_NAME\"" >> bin/activate
    echo "export PIP_RESPECT_VIRTUALENV=true" >> bin/activate
    echo "export PYTHONPATH=\"\$VIRTUAL_ENV/repo/src\"" >> bin/activate
    echo "unset DJANGO_SETTINGS_MODULE" >> bin/activate

    # Activate the environment.
    source bin/activate

    # Initialize a git repository in the `repo` subdirectory of this virtualenv
    git init repo
    cd repo

    # Start this git repo with my Python .gitignore of choice.
    # See it at https://gist.github.com/1806643/ for notes.
    curl -sLO https://raw.github.com/gist/1806643/.gitignore
    git add .gitignore
    git commit -m "initial commit, .gitignore"

    # Create a `src` directory within our repo.
    mkdir src

    # Install Django (1.3.X), gunicorn (0.13.X), gevent (0.13.X), and the greenlet
    # dependency.
    echo "django==1.3.1" > requirements.txt
    echo "gunicorn==0.13.4" >> requirements.txt
    echo "gevent==0.13.4" >> requirements.txt
    echo "greenlet==0.3.4" >> requirements.txt
    pip install -r requirements.txt

    # Enter the `src` dir and create a django project
    cd $VIRTUAL_ENV/repo/src
    $VIRTUAL_ENV/bin/django-admin.py startproject $PYTHON_APP_NAME
    cd $VIRTUAL_ENV/repo

    # Unlike the gunicorn defined in Heroku's Django example, we're going
    # to use one of the async worker classes, "gevent". Using an async worker class
    # is recommended when serving traffic directly to gunicorn (which is what
    # happens under the Heroku Cedar stack).
    echo "web: gunicorn_django -b 0.0.0.0:\$PORT -w 9 -k gevent --max-requests 250 --preload src/$PYTHON_APP_NAME/settings.py" > Procfile

    # Commit everything we have in here.
    git add .
    git commit -m "base django site"

    # Test out our setup.
    foreman start
    # ... test in browser: http://127.0.0.1:5000/

    # Create a Heroku instance for this site
    heroku create -s cedar $PROJECT_NAME

    # Make sure to add `src` to the PYTHONPATH on our server. (We added this to our
    # local activate file, but it needs to be applied to Heroku, too.)
    heroku config:add PYTHONPATH=/src

    # Deploy this project to Heroku
    git push heroku master

### Configuring a database and serving static files

    heroku addons:add shared-database:5mb

    cd $VIRTUAL_ENV/repo
    echo "psycopg2" >> requirements.txt
    echo "boto==2.2.1" >> requirements.txt
    echo "django-storages==1.1.4" >> requirements.txt
    pip install -r requirements.txt

Open settings.py, add `'storages'` to `INSTALLED_APPS`, uncomment `django.contrib.admin`.

Add these to settings.py, filling in your own `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY`, and `AWS_STORAGE_BUCKET_NAME`:

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    AWS_STORAGE_BUCKET_NAME = ''
    STATIC_URL = '//s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

Add to end of settings.py:

    import os
    import sys
    import urlparse

    # Register database schemes in URLs.
    urlparse.uses_netloc.append('postgres')
    urlparse.uses_netloc.append('mysql')

    try:
        if 'DATABASES' not in locals():
            DATABASES = {}

        if 'DATABASE_URL' in os.environ:
            url = urlparse.urlparse(os.environ['DATABASE_URL'])

            # Ensure default database exists.
            DATABASES['default'] = DATABASES.get('default', {})

            # Update with environment configuration.
            DATABASES['default'].update({
                'NAME': url.path[1:],
                'USER': url.username,
                'PASSWORD': url.password,
                'HOST': url.hostname,
                'PORT': url.port,
            })
            if url.scheme == 'postgres':
                DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

            if url.scheme == 'mysql':
                DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'
    except Exception:
        print 'Unexpected error:', sys.exc_info()

Open urls.py and uncomment the lines for the admin.

    git add .
    git commit -m "enable admin and boto-backed storage"

    # deploy
    git push heroku master

    heroku run "python src/$PYTHON_APP_NAME/manage.py collectstatic --noinput"

    heroku run "python src/$PYTHON_APP_NAME/manage.py syncdb --noinput"
    heroku run "python src/$PYTHON_APP_NAME/manage.py createsuperuser"

### Adding cache

    heroku addons:add memcache:5mb

    cd $VIRTUAL_ENV/repo
    echo "pylibmc==1.2.2" >> requirements.txt
    echo "django-pylibmc-sasl==0.2.4" >> requirements.txt
    pip install -r requirements.txt

Add to settings.py:


    CACHES = {
        'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache'
        }
    }

Then deploy

    git add .
    git commit -m "cache"
    git push heroku master

### Adding (and enforcing) SSL

    heroku addons:add ssl:piggyback

Download [this SSL middleware][ssl_middleware] and add it to `MIDDLEWARE_CLASSES`
in settings.py

[ssl_middleware]: https://gist.github.com/1812422

Then deploy

    git add .
    git commit -m "cache"
    git push heroku master
