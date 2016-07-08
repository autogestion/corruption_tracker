# import time
import datetime
import uuid

from django.db import connection


def request_id(request):
    if not hasattr(request, "request_id"):
        request.request_id = uuid.uuid4().__str__()

    return request.request_id


class SqlProfilingMiddleware():
    Queries = []

    def process_request(self, request):
        self.request_started = datetime.datetime.now()
        SqlProfilingMiddleware.Queries.insert(0, {"time": 15 * 'o',
            "sql": 10 * '-', 'type': 'delimeter', 'request_id': 35 * 'o'})
        SqlProfilingMiddleware.Queries.insert(0, {"time": self.request_started.strftime('%H:%M:%S %f'),
            "sql": request.path, 'type': 'request_started', 'request_id': request_id(request)})
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    # def process_template_response(self, request, response):
    #     self._add_sql_queries(request)
    #     return response

    def process_response(self, request, response):
        self._add_sql_queries(request)
        responce_rendered = datetime.datetime.now()
        request_total = responce_rendered - self.request_started
        # print('request cycle', request_total)
        SqlProfilingMiddleware.Queries.insert(0, {"time": responce_rendered.strftime('%H:%M:%S %f'),
            "sql": request.path, 'type': 'responce_rendered', 'request_id': request_id(request)})
        SqlProfilingMiddleware.Queries.insert(0, {"time": request_total,
            "sql": request.path, 'type': 'request_total', 'request_id': request_id(request)})

        response['executed'] = request_total
        return response

    def process_exception(self, request, exception):
        return None

    def _add_sql_queries(self, request):
        for q in connection.queries:
            # q["time"] = time.time() + float(q["time"])
            q['type'] = 'sql_query'
            q['request_id'] = request_id(request)
            SqlProfilingMiddleware.Queries.insert(0, q)
