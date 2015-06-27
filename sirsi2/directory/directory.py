import requests
from . import models
from ..common import parse_response, api_response

DIRECTORY_ENDPOINT = 'http://directory.sirsidynix.net/libdir/rest/v4/{}'
CLIENT_ID = 'iPatronId'
USER_AGENT = 'BookMyne/20131010 CFNetwork/711.1.12 Darwin/14.0.0'

def call(method, parameters=None):
    if parameters is None:
        parameters = {}
    headers = {
        'x-sirs-clientID': CLIENT_ID,
        'x-sirs-locale': 'en_US',
        'User-Agent': USER_AGENT,
    }
    return requests.get(
        DIRECTORY_ENDPOINT.format(method),
        params=parameters,
        headers=headers
    )

def get_listings_birthday():
    res = call('getListingsBirthday')
    return api_response(int(res.text), res)

def get_brief_libraries(version=1):
    res = call('getBriefLibraries', parameters={'version': version})
    return api_response(parse_response(res, models.GetBriefLibrariesResponse),
                        res)

def get_library(id):
    res = call('getLibrary', parameters={'id': id})
    return api_response(parse_response(res, models.GetLibraryResponse), res)
