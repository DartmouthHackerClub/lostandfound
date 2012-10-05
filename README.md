Lost and Found
==============================

Uses flask CAS Template

Introduction
----------

Features include:

Setup
-----


Assuming you already have Python and pip installed, go ahead and install
`virtualenv` if you haven't already:

    $ sudo pip install virtualenv

Now, create a new virtualenv (this provides an isolated environment for
the app to run in):

    $ virtualenv lostandfound
    $ cd lostandfound
    $ source bin/activate

The virtualenv is now set up. You can clone this repository inside the
virtualenv:

    $ git clone https://github.com/DartmouthHackerClub/lostandfound.git

I've included a `requirements.txt` file, which, coupled with pip and
virtualenv, provides an automatic method for installing all necessary
dependencies:

    $ cd lostandfound
    $ pip install -r requirements.txt

To change the settings before running, you must do the following:

    $ nano default_settings.py

Edit settings and save as local_settings.py

Everything should now set up. You can now launch the app:

    $ python app.py

Check out the [Flask docs](http://flask.pocoo.org/) to learn where you
can go from here.

Deployment
----------

I recommend using several [gunicorn](http://gunicorn.org/) instances
behind nginx. This works as follows:

### Launch the gunicorn app server

    $ gunicorn app:app -b 127.0.0.1:1337 -w 2

Two gunicorn worker processes will be launched and bound to port 1337.
The `app:app` part refers to the `app` variable (i.e. the `Flask`
object) within `app.py`.

Notice that gunicorn will only serve requests originating from localhost
-- this is ideal because gunicorn is not meant to be accessed directly
(except by nginx, which is on localhost).

### Configure nginx as a reverse proxy to gunicorn

    server {
        server_name app.hacktown.cs.dartmouth.edu;
        root /srv/http/app.hacktown.cs.dartmouth.edu/public;

        location / {
            try_files $uri @gunicorn;
            index index.html index.htm;
        }

        location @gunicorn {
            proxy_pass         http://127.0.0.1:1337/;
            proxy_redirect     off;
            proxy_set_header   Host             $host;
            proxy_set_header   X-Real-IP        $remote_addr;
            proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        }
    } 

This configuration will first try to directly serve a static file if it
exists, and if not, proxy the request to gunicorn. In other words, if
you put static assets in
`/srv/http/app.hacktown.cs.dartmouth.edu/public`, they will be served
efficiently by nginx and not by gunicorn.

### Set up process control

Now the app should be available at
http://app.hacktown.cs.dartmouth.edu/. However, what happens if the
machine is restarted or if gunicorn is terminated abnormally? You will
get a 503 error because gunicorn isn't running. We need something that
will automatically restart gunicorn if it isn't running for some reason.
We need a process control system.

The process control system I use is
[Supervisor](http://supervisord.org/). Once you've got it installed, you
can use the following configuration to keep gunicorn running all the
time:

    [program:app_name]
    command = /home/deploy/env/app_name/bin/gunicorn app:app -b 127.0.0.1:1337 -w 2
    directory = /home/deploy/env/app_name/app_name
    user = deploy

### Automate updates with fabric

I've included a `fabfile.py` which greatly simplifies pushing new code
to the staging and production servers. To deploy the latest code to the
testing server:

    $ fab test deploy

Or to the production server:

    $ fab prod deploy
