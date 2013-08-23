import json
from regenesis.queries import get_cubes, get_all_dimensions, get_dimensions
from pprint import pprint


def generate_dimensions():
    dimensions = []
    for dimension in get_all_dimensions():
        pprint (dimension)
        if dimension.get('measure_type').startswith('W-'):
            continue
        attrs = ['name', 'label']
        if 'ZI' in dimension.get('measure_type'):
            attrs = ['text', 'from', 'until']
        dim = {
            'name': dimension.get('name'),
            'label': dimension.get('title_de'),
            'description': dimension.get('definition_de'),
            'attributes': attrs
        }
        dimensions.append(dim)
    return dimensions


def generate_cubes():
    cubes = []
    for cube in get_cubes():
        dimensions = []
        measures = []
        joins = []
        mappings = {}
        cube_name = cube.get('cube_name')
        for dim in get_dimensions(cube_name):
            dn = dim.get('dim_name')
            if dim.get('dim_measure_type').startswith('W-'):
                measures.append(dn)
                continue
            
            dimensions.append(dn)
            if dim.get('dim_measure_type').startswith('ZI-'):
                mappings[dn + '.text'] = 'fact_%s.%s' % (cube_name, dn)
                mappings[dn + '.from'] = 'fact_%s.%s_from' % (cube_name, dn)
                mappings[dn + '.until'] = 'fact_%s.%s_until' % (cube_name, dn)
            else:
                tn = 'tbl_' + dn
                joins.append({
                    'master': dn,
                    'detail': 'value.value_id',
                    'alias': tn
                    })
                mappings[dn + '.name'] = tn + '.name'
                mappings[dn + '.label'] = tn + '.title_de'

            
        cubes.append({
            'dimensions': dimensions,
            'measures': measures,
            'mappings': mappings,
            'joins': joins,
            'fact': 'fact_%s' % cube_name,
            'name': cube.get('cube_name'),
            'label': cube.get('statistic_title_de'),
            'description': cube.get('statistic_description_de'),
            })
    return cubes


def generate_model():
    model = {
        'dimensions': generate_dimensions(),
        'cubes': generate_cubes(),
        'locale': 'de'
    }
    pprint(model)
    return model
    

if __name__ == '__main__':
    with open('model.json', 'wb') as fh:
        model = generate_model()
        json.dump(model, fh, indent=2)

