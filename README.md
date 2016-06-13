# Corruption tracker

Corruption tracker lets you make cases of corruption and professionally unfit of civil servant public
and as result track the level of it in public institutions

![](http://i.imgur.com/zAMVod3.png)

Mobile app that works with API https://github.com/konchunas/mobilepdrk

Demo http://beta.acts.pp.ua/

FB - https://www.facebook.com/activecorruptiontracking/

Prerequisites

    Python 3.5
    PostgreSQL + PostGIS
    Memcached

## Quickstart on Ubuntu 16.04

Install dependencies and project

    sudo apt-get install git supervisor nginx python3-dev python3-venv libpq-dev postgresql postgresql-contrib postgis memcached

    python3.5 -m venv ctracker
    . ctracker/bin/activate

    git clone git@github.com:autogestion/corruption_tracker.git && cd corruption_tracker
    pip install -r requirements.txt

Create local settings file

    cp corruption_tracker/local_settings.py.sample  corruption_tracker/local_settings.py

Create the tables

    PostgreSQL instructions in db_creation.txt

    python manage.py migrate
    python manage.py createsuperuser
    python manage.py initiate_db

Start the server

    python manage.py runserver 0.0.0.0:8000

## Submit a bug

We would like to hear about any bugs or odd behavior that you uncover. Use the [issue tracker](../../issues/) to open a new item. When describing the issue, we recommend that you discuss the following items:

  * Describe the bug
  * Describe the steps you did to discover the bug
  * What was the expected outcome of the above steps?
  * Please provide screenshots, if applicable     

## FRONTEND SINGLE-PAGE REALISATION WITH REACT

## Requirements
- ``` $ node -v ``` is a **^4.2.0**

- ``` $ npm -v ``` is a **^3.0.0**


## Instalation

```
$ npm install
$ npm run start
$ npm run devserver
```
Open your browser at http://localhost:3030.



## Development
- ``` $ npm run start ``` - Provides **compiled** bundles to 'public' directory.

- ``` $ npm run devserver ``` - Runs the project in development mode with hot-reloading of 'public' folder. Open your browser at http://localhost:3030.

- ``` $ npm run build ``` - Provide **compiled**, and **minified** bundles to 'public' directory.

- ``` npm run test ``` - Runs tests **once** with Mocha(server side interpretation). Entry point: **'test/setup.js'**.

- ``` npm run test:watch ``` - **Continuously** watch changes and run tests immediately after changes.


- ``` npm run test:TeamCity ``` - Provides tests coverage report to TeamCity build system.


- ``` npm run lint ``` - Runs eslint checker **once**. Entry point: **'.eslintrc'**.

- ``` npm run lint:watch ``` - **Continuously** watch changes and run Run eslint checker immediately after some changes.

- ``` npm run clear ``` - Remove 'public' and 'node_modules' folders.
