# Corruption tracker

Corruption tracker lets you make cases of corruption and professionally unfit of civil servant public
and as result track the level of it in public institutions

![](http://i.imgur.com/zAMVod3.png)

Mobile app that works with API https://github.com/konchunas/mobilepdrk

Test instance available on http://test.acts.pp.ua:8000/

Test api is available on http://test.acts.pp.ua:8000/api/docs/

FB - https://www.facebook.com/activecorruptiontracking/

Prerequisites

    Python 3.4
    PostgreSQL + PostGIS
    Memcached

## Quickstart

Create a virtual environment

    virtualenv --python=/usr/bin/python3.4 ctracker
    source ctracker/bin/activate

Install dependencies and project

    sudo apt-get install python3.4-dev libpq-dev postgresql postgresql-contrib postgis postgresql-9.5-postgis-2.2 memcached
    git clone git@github.com:autogestion/corruption_tracker.git
    cd YOUR_SOURCE_DIR
    pip install -r requirements.txt

Create a default local settings file

    cp corruption_tracker/local_settings.py.sample  corruption_tracker/local_settings.py

Create the tables

    PostgreSQL instructions in db_creation.txt

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py initiate_db

Start the server

    python manage.py runserver 0.0.0.0:8000
