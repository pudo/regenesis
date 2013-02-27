from datetime import datetime
import json

class JSONEncoder(json.JSONEncoder):
    """ This encoder will serialize all entities that have a to_dict
    method by calling that method and serializing the result. """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        raise TypeError("%r is not JSON serializable" % obj)


