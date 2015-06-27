from __future__ import absolute_import
import requests
from . import models
from ..common import parse_response, depends_on, api_response, raise_
from hashlib import md5

SYMPHONYWS_ENDPOINT = '{}/rest/{}'
HEADERS_TEMPLATE = {
    'x-sirs-clientID': 'sdIPhoneApp',
    'x-sirs-locale': 'en_US',
    'User-Agent': 'BookMyne/20131010 CFNetwork/711.1.12 Darwin/14.0.0',
}

def call(symphonyws_url, method, parameters=None, headers=None):
    h = dict(HEADERS_TEMPLATE)
    h.update({} if headers is None else headers)
    return requests.get(
        SYMPHONYWS_ENDPOINT.format(symphonyws_url, method),
        params={} if parameters is None else parameters,
        headers=h,
    )

def make_client_passthrough_token(server_token):
    s = '{}s1rs1F&n9533'.format(server_token).encode('utf-8')
    return md5(s).hexdigest()

class SymphonyWsAPI():

    def __init__(self, symphonyws_url):
        self.symphonyws_url = symphonyws_url
        self.server_passthrough_token = None
        self.session_token = None
        self.last_response = None

    @property
    def client_passthrough_token(self):
        if not self.server_passthrough_token:
            return
        return make_client_passthrough_token(self.server_passthrough_token)

    def call(self, method, parameters=None, headers=None):
        res = call(self.symphonyws_url, method, parameters, headers)
        self.last_response = res
        return res

    def passthrough_call(self, method, parameters=None, headers=None):
        h = {} if headers is None else headers
        h['x-sirs-passthrough'] = self.client_passthrough_token
        return self.call(method, parameters, h)

    def authenticated_call(self, method, parameters=None, headers=None):
        h = {} if headers is None else headers
        h['x-sirs-sessionToken'] = self.session_token
        return self.call(method, parameters, h)

    def admin_lookup_native_currency(self):
        res = self.call('admin/lookupNativeCurrency')
        return api_response(res.text.strip(), res)

    def admin_lookup_ils_configuration(self, config_name):
        res = self.call(
            'admin/lookupILSConfiguration',
            {'configName': config_name},
        )
        parsed = parse_response(res, models.LookupILSConfigurationResponse)
        return api_response(parsed, res)

    def standard_version(self):
        res = self.call('standard/version')
        return api_response(parse_response(res, models.VersionResponse), res)

    def security_get_passthrough_token(self, save=True):
        res = self.call('security/getPassthroughToken')
        passthrough = res.text.strip()
        if save:
            self.server_passthrough_token = passthrough
        return api_response(passthrough, res)

    @depends_on('client_passthrough_token',
                lambda self: self.security_get_passthrough_token())
    def security_login_user(self, login, password, save=True):
        parameters = {
            'login': login,
            'password': password,
        }
        res = self.passthrough_call('security/loginUser', parameters)
        parsed = parse_response(res, models.LoginUserResponse)
        if save and parsed.meta.tagname == 'LoginUserResponse':
            self.session_token = parsed.sessionToken
        return api_response(parsed, res)

    @depends_on('session_token',
                lambda: raise_(RuntimeError('Please populate self.session_token'
                                           ' or call self.security_login_user '
                                           'first.')))
    def patron_lookup_my_account_info(self, library_station=None, include=None):
        if include is None:
            include = {
                'PatronCheckout': 'ALL',
                'PatronAddress': 'true',
                'Fee': 'UNPAID_FEES_AND_PAYMENTS',
                'PatronHold': 'ACTIVE',
                'PatronCirculation': 'true',
                'Patron': 'true',
            }
        p = {''.join(['include', k, 'Info']): v for k, v in include.items()}
        if library_station is not None:
            p['libraryStation'] = library_station
        res = self.authenticated_call('patron/lookupMyAccountInfo', parameters=p)
        parsed = parse_response(res, models.LookupMyAccountInfoResponse)
        return api_response(parsed, res)

    def patron_renew_my_checkout(self, item_id):
        res = self.authenticated_call('patron/renewMyCheckout',
                                      parameters={'itemID': item_id})
        parsed = parse_response(res, models.RenewMyCheckoutResponse)
        return api_response(parsed, res)
