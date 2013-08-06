
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