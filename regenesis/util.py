from datetime import datetime
from hashlib import sha1
from unicodedata import normalize as ucnorm, category


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


def flatten(d, sep='_'):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            for ik, iv in flatten(v, sep=sep).items():
                out[k + sep + ik] = iv
        else:
            out[k] = v
    return out


def slugify(text):
    if not isinstance(text, unicode):
        text = unicode(text)
    text = text.lower()
    decomposed = ucnorm('NFKD', text)
    filtered = []
    for char in decomposed:
        cat = category(char)
        if char == "'" or cat.startswith('M') or cat.startswith('S'):
            continue
        elif cat.startswith('L') or cat.startswith('N'):
            filtered.append(char)
        else:
            filtered.append('-')
    text = u''.join(filtered)
    while '--' in text:
        text = text.replace('--', '-')
    text = text.strip()
    return ucnorm('NFKC', text)
