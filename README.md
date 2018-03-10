Grorg
-----

[![Build Status](https://travis-ci.org/raiderrobert/grorg.svg?branch=master)](https://travis-ci.org/raiderrobert/grorg)

A semi-experimental platform for managing grant applications.

The running copy is at http://grorg.aeracode.org - contact andrew@aeracode.org to set up access.


Deploy on Heroku
================

    git clone git@github.com:andrewgodwin/grorg.git
    cd grorg
    heroku login
    heroku create myappname  # Replace with your own name
    heroku config:set DJANGO_SECRET_KEY=asdfasdf  # Use a random one
    heroku config:set DJANGO_SETTINGS_MODULE=grorg.heroku_settings
    git push heroku master
    heroku run python manage.py migrate
    heroku run python manage.py createsuperuser  # Create your own superuser
    heroku open  # Have fun
