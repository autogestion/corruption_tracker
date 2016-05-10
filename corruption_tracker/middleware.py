from django.db import connection
import time
import datetime


def started(sender, **kwargs):
    global started
    started = datetime.datetime.now()

def finished(sender, **kwargs):
    global total
    total = datetime.datetime.now() - started

from django.core import signals

signals.request_started.connect(started)
signals.request_finished.connect(finished)


class SqlProfilingMiddleware():
    Queries = []

    def process_request(self, request):
        return None
    def process_view(self, request, view_func, view_args, view_kwargs):
        return None
    def process_template_response(self, request, response):
        self._add_sql_queries(request)
        return response
    def process_response(self, request, response):
        self._add_sql_queries(request)
        return response
    def process_exception(self, request, exception):
        return None

    def _add_sql_queries(self, request):
        SqlProfilingMiddleware.Queries.insert(0, {"time": started.strftime('%H:%M:%S %f'), "sql" : request.path, 'type': 'request_started'})
        for q in connection.queries:
            q["time"] = time.time() + float(q["time"])
            q['type'] = 'sql_query'
            # q["time"] =  float(q["time"])
            SqlProfilingMiddleware.Queries.insert(0, q)
            # add request info as a separator
        SqlProfilingMiddleware.Queries.insert(0, {"time": datetime.datetime.now().strftime('%H:%M:%S %f'), "sql" : request.path, 'type': 'log_created'})
        
        try:
            SqlProfilingMiddleware.Queries.insert(0, {"time": started.strftime('%H:%M:%S %f'), "sql" : request.path, 'type': 'request_total'})
        except NameError:
            pass