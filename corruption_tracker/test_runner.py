from django.test.runner import DiscoverRunner, get_unique_databases_and_mirrors
from django.db import connections

class DefaultDbTestRunner(DiscoverRunner):
    """ A test runner to test without database creation/deletion 

    python manage.py test --testrunner=corruption_tracker.test_runner.DefaultDbTestRunner

    """

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass



import datetime
from pprint import pprint

from django.test import Client
from django.test.utils import override_settings

from corruption_tracker.middleware import SqlProfilingMiddleware


@override_settings(DEBUG=True)
def perfomance_test(url, request_type='get'):
    c = Client()
    response = getattr(c, request_type)(url)

    print(response.status_code)
    pprint(SqlProfilingMiddleware.Queries)

    request_started = datetime.datetime.now()
    for x in range(100):
        getattr(c, request_type)(url)
        if x==50:
            print('\n', '50x ', datetime.datetime.now()-request_started)

    print('\n', '100x ', datetime.datetime.now()-request_started)


