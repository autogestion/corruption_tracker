import json


def get_geojson_file(file_path):
    # print(file_path)
    try:
        # python 3+
        json_s = open(file_path, encoding='utf8').read()
    except TypeError:
        # python 2
        json_s = open(file_path).read()
        json_s = json_s.decode('utf8')

    return json.loads(json_s)


# TODO(vegasq) Need create utils module, or something similar.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
