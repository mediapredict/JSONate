try:
    import json
except ImportError:
    from django.utils import simplejson as json

from .json_encoder import UUIDEncoder
from django.db.models.fields.related import ManyToManyField


def jsonate(obj, *args, **kwargs):
    kwargs['cls'] = UUIDEncoder
    return json.dumps(obj, *args, **kwargs)


def serialize(instance):
        # Use this to process instances with Many to Many relations.
        # returns all fields and pk for relations in dict form {}
        # use case -> jsonate(serialize(instance))
        opts = instance._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if instance.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = [inst.pk for inst in f.value_from_object(instance)]
            else:
                data[f.name] = f.value_from_object(instance)
        return data