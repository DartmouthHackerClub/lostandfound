The Hacker Club Flask Template
==============================

Introduction
------------

This template provides a starting point for new Hacker Club Flask
projects.

Features include:

-   Dartmouth CAS authentication pre-configured
-   Latest Twitter Bootstrap and jQuery from CDN
-   Jinja2 templating pre-configured

Usage
-----

Assuming you already have Python and pip installed, go ahead and install
`virtualenv` if you haven't already:

    $ sudo pip install virtualenv

Now, create a new virtualenv (this provides an isolated environment for
the app to run in):

    $ virtualenv <project_name>
    $ cd project_name
    $ source bin/activate

The virtualenv is now set up. You can clone this repository inside the
virtualenv:

    $ git clone https://github.com/DartmouthHackerClub/flask_template.git

I've included a `requirements.txt` file, which, coupled with pip and
virtualenv, provides an automatic method for installing all necessary
dependencies:

    $ cd flask_template
    $ pip install -r requirements.txt

Everything is now set up. You can now launch the app:

    $ python app.py

Check out the [Flask docs](http://flask.pocoo.org/) to learn where you
can go from here.
