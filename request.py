import requests


class BadRequest(Exception):
    def __init__(self, request, status, reason):
        super().__init__()
        self.request = request
        self.status = status
        self.reason = reason

    def __str__(self):
        msg = 'Request failed:\n%s\nHttp status: %s (%s)' %\
              (self.request, self.status, self.reason)
        return msg


# static maps api request
def static_maps(**kwargs):
    api_server = 'https://static-maps.yandex.ru/1.x/'
    response = requests.get(api_server, params=kwargs)
    if not response:
        raise BadRequest(api_server, response.status_code, response.reason)

    return response.content


# geocoder api request
def geocoder(**kwargs):
    api_server = 'https://geocode-maps.yandex.ru/1.x'
    kwargs['format'] = 'json'

    response = requests.get(api_server, params=kwargs)
    if not response:
        raise BadRequest(api_server, response.status_code, response.reason)

    json_response = response.json()
    objects = json_response['response']['GeoObjectCollection']['featureMember']
    if not objects:
        return []
    for i in range(len(objects)):
        objects[i] = objects[i]['GeoObject']

    return objects


# geosearch api request
def geosearch(**kwargs):
    api_server = 'https://search-maps.yandex.ru/v1/'
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'

    kwargs['lang'] = 'ru_RU'
    kwargs['apikey'] = api_key

    response = requests.get(api_server, params=kwargs)
    if not response:
        raise BadRequest(api_server, response.status_code, response.reason)

    json_response = response.json()
    objects = json_response['features']

    return objects
