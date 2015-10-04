# Corruption tracker

## About

Corruption tracker lets you make cases of corruption and professionally unfit of civil servant public
and as result track the level of it in public institutions

![impl](https://cloud.githubusercontent.com/assets/1098257/10265887/8a21a9f0-6a4a-11e5-8c8c-bf12e7422347.png)


Prerequisites

    Python 3.4
    Memcached

## Quickstart

Create a virtual environment

    virtualenv --python=/usr/bin/python3.4 ctracker
    source ctracker/bin/activate

Install dependencies and project

    git clone git@github.com:autogestion/corruption_tracker.git
    cd YOUR_SOURCE_DIR
    pip install -r requirements.txt

Create a default local settings file

    cp corruption_tracker/local_settings.py.sample  corruption_tracker/local_settings.py

Create the tables

    python manage.py syncdb
    python manage.py initiate_db

Start the server

    python manage.py runserver 0.0.0.0:8000
