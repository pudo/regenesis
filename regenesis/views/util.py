import re

SPLITTER = re.compile('\n(\d.*):\s', re.M)

def dimension_type_text(type_name):
    if type_name.startswith('ZI-MM'):
        return 'Zeitattribut'
    if type_name.startswith('K-REG'):
        return 'Geographisches Attribut'
    if type_name.startswith('K-SACH'):
        return 'Sachattribut'
    if type_name.startswith('W-MM'):
        return 'Messwert'
    return type_name


def parse_description(description):
    description = '\n' + description
    parts = SPLITTER.split(description)[1:]
    data = {'method': 'Keine Angaben.', 'type': 'Keine Angaben.'}
    for i in range(0, len(parts), 2):
        section, text = parts[i], parts[i+1].strip()
        if 'Art der Statistik' in section:
            data['type'] = text
        elif 'Rechtsgrundlage' in section:
            data['legal'] = text
        elif 'Bereitstellung' in section:
            data['periodicity'] = text
        elif 'Stichtag' in section:
            data['stag'] = text
        elif 'Regionalebene' in section:
            data['geo'] = text
        elif 'Methodische' in section:
            data['method'] = text
    return data

