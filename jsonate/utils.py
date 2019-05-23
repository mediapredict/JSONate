try:
    import json
except ImportError:
    from django.utils import simplejson as json

from .json_encoder import UUIDEncoder


def jsonate(obj, *args, **kwargs):
    kwargs['cls'] = UUIDEncoder
    return json.dumps(obj, *args, **kwargs)