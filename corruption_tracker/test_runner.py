import time
from pprint import pprint

from django.test import Client
from django.test.utils import override_settings
from django.test.runner import DiscoverRunner

class DefaultDbTestRunner(DiscoverRunner):
    """ A test runner to test without database creation/deletion

    python manage.py test --testrunner=corruption_tracker.test_runner.DefaultDbTestRunner

    """

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass


@override_settings(DEBUG=True)
def perfomance_test(url, request_type='get'):
    c = Client()
    response = getattr(c, request_type)(url)

    print(response.status_code)
    request_started = time.time()
    for x in range(100):
        getattr(c, request_type)(url)
        if x == 50:
            print('\n', '50x ', time.time() - request_started)

    print('\n', '100x ', time.time() - request_started)
