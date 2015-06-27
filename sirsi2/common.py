from dexml import Model, ParseError
from dexml.fields import Boolean, String, List, Integer
from collections import namedtuple

REST_NS = 'http://schemas.sirsidynix.com/rest'

api_response = namedtuple('api_response', ['data', 'response'])

class Fault(Model):
    class meta():
        namespace = REST_NS

    code = String(tagname='code')
    string = String(tagname='string')

def parse_response(res, model):
    first_ex = None
    try:
        return model.parse(res.text)
    except ParseError as ex:
        first_ex = ex
    try:
        return Fault.parse(res.text)
    except ParseError:
        # If it isn't a Fault, then there is probably a bug in the target model.
        raise first_ex

def depends_on(attr, lambda_):
    def outer(fn):
        def inner(self, *args, **kwargs):
            if getattr(self, attr) is None:
                lambda_(self)
            return fn(self, *args, **kwargs)
        return inner
    return outer

def raise_(ex):
    raise ex
