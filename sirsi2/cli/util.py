import os.path
import json
from ..symphonyws import SymphonyWsAPI

def load_settings(path=None):
    if path is None:
        path = os.path.expanduser('~/.sirsi.json')
    with open(path) as f:
        return json.load(f)

def construct_api():
    settings = load_settings()
    return (SymphonyWsAPI(settings['symphonyws_url']), settings)

def construct_api_and_login():
    ret = construct_api()
    ret[0].security_login_user(ret[1]['userid'], ret[1]['password'])
    return ret

def renew_my_books():
    api, _ = construct_api_and_login()
    res = api.patron_lookup_my_account_info()
    xml = res.data
    renewals = [(api.patron_renew_my_checkout(i.itemID), i) for i in xml.patronCheckoutInfos if i.renewalsRemaining > 0]
    for r in renewals:
        renewed = r[0].data.meta.tagname != 'Fault'
        t = 'renewed' if renewed else 'not renewed'
        due = r[0].data.dueDate if renewed else r[1].dueDate
        print('{} by {} was {} (due {}).'.format(r[1].title, r[1].author, t, due))
