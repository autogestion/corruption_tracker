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