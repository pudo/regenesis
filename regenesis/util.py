from datetime import datetime
from hashlib import sha1

def make_key(*a):
    parts = []
    for part in a:
        if isinstance(part, datetime):
            part = part.isoformat()
        elif part is None:
            part = '**'
        else:
            part = unicode(part)
        parts.append(part)
    return sha1('||'.join(parts)).hexdigest()
