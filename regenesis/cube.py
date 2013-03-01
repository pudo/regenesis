from collections import defaultdict
from csv import reader
from StringIO import StringIO

from regenesis.mappings import KEYS_TRANSLATE, KEYS_IGNORE, KEYS_LOCALIZED
from regenesis.formats import parse_date, parse_bool
from regenesis.util import make_key, flatten

FIELD_TYPES = {
  'eu_vbd': parse_bool,
  'genesis_vbd': parse_bool,
  'regiostat': parse_bool,
  'secret_values': parse_bool,
  'spr_tmp': parse_bool,
  'regiostat': parse_bool,
  'trans_flag_2': parse_bool,
  'meta_variable': parse_bool,
  'summable': parse_bool,
  'atemporal': parse_bool,
  'valid_from': lambda d: parse_date(d)[0],
  'valid_until': lambda d: parse_date(d)[1],
  'pos_nr': int,
  'axis_order': int,
  'label_order': int,
  'float_precision': int
  }

class Section(object):

    def __init__(self, data):
        self._header = data[0].split(';')
        self._data = data[1:]
        self._rows = None

    @property
    def columns(self):
        columns = []
        for col in self._header[1:]:
            col = col.lower().replace('-', '_')
            col = KEYS_TRANSLATE.get(col, col)
            columns.append(col)
        return columns

    @property
    def rows(self):
        if self._rows is None:
            plain = '\n'.join(self._data).encode('utf-8')
            plain = plain.replace(';\n"', ';"')
            csv = reader(StringIO(plain), delimiter=';')
            self._rows = []
            for row in csv:
                row = [r.decode('utf-8') for r in row]
                self._rows.append(row[1:])
        return self._rows

    def __iter__(self):
        for data in self.rows:
            obj = {}
            is_translated = True
            for key, value in zip(self.columns[1:], data):
                if not len(value):
                    continue
                if key in FIELD_TYPES:
                    value = FIELD_TYPES[key](value)
                if key == 'trans_flag_2':
                    is_translated = value
                if key in KEYS_IGNORE:
                    continue
                obj[key] = value
            if not is_translated:
                for key in KEYS_LOCALIZED:
                    if key in obj:
                        del obj[key]
            yield obj

    @property
    def first(self):
        objs = list(self)
        assert len(objs)==1, 'first() on multi-row data!'
        return objs[0]


class Fact(object):

    def __init__(self, cube, row):
        self.cube = cube
        self.row = row

    @property
    def mapping(self):
        offset = 0
        mapping = {}
        identity_parts = []
        for axis in self.cube.axes:
            mapping[axis.name] = self.row[offset].lower()
            identity_parts.append(self.row[offset])
            offset += 1

        for time in self.cube.times:
            time_from, time_until = parse_date(self.row[offset])
            identity_parts.append(self.row[offset])
            mapping[time.name] = {
                'value': self.row[offset],
                'from': time_from,
                'until': time_until
                }
            offset += 1

        for measure in self.cube.measures:
            m = {}
            if measure.data_type == 'GANZ':
                m['value'] = int(self.row[offset])
            else:
                m['value'] = float(self.row[offset])
            m['quality'] = self.row[offset+1]
            m['locked'] = self.row[offset+2]
            m['error'] = self.row[offset+3]
            mapping[measure.name] = m
            offset += 4

        mapping['fact_id'] = make_key(*identity_parts)
        return mapping

    @property
    def time(self):
        return self.mapping.get(self.cube.times[0].name)

    def get_value(self, dimension, value):
        return self.cube.dimensions[dimension].find_value(value,
                self.time.get('from'), self.time.get('until'))

    def to_row(self):
        out, values = {}, {}
        for key, value in self.mapping.items():
            if isinstance(value, dict) and 'value' in value:
                values[key] = value.get('value')
                del value['value']
            if not isinstance(value, dict) and key != 'fact_id':
                value = self.get_value(key, value) 
                if value is not None:
                    value = value.id
            out[key] = value
        out = flatten(out)
        out.update(values)
        return out

    def to_dict(self):
        return self.mapping
        #return self.to_row()

    def __repr__(self):
        return repr(self.mapping)


class Value(object):

    def __init__(self, dimension, base_data, assoc_data):
        self.dimension = dimension
        self.data = base_data.copy()
        self.data.update(assoc_data)
        self.data['name'] = self.data.get('key').lower()
        del self.data['key']

    @property
    def id(self):
        return make_key(self.dimension.name,
                        self.data.get('name'),
                        self.data.get('valid_from'),
                        self.data.get('valid_until'))

    def match(self, name, begin_time, end_time):
        if name != self.data.get('name'):
            return False
        if begin_time and self.data.get('valid_from') and \
            begin_time < self.data.get('valid_from'):
            return False
        if end_time and self.data.get('valid_until') and \
            end_time > self.data.get('valid_until'):
            return False
        return True

    def to_row(self):
        d = self.to_dict()
        return d

    def to_dict(self):
        d = self.data.copy()
        d['dimension_name'] = self.dimension.name
        d['value_id'] = self.id
        return d


class Dimension(object):

    def __init__(self, cube, data):
        self.cube = cube
        data['name'] = data['name'].lower()
        self.data = data
        self.values = []

    @property
    def name(self):
        return self.data.get('name')

    def add_value(self, base_data, assoc_data):
        self.values.append(Value(self, base_data, assoc_data))

    def find_value(self, key, begin_time, end_time):
        for value in self.values:
            if value.match(key, begin_time, end_time):
                return value

    def to_dict(self):
        d = self.data.copy()
        d['values'] = self.values
        return d

    def to_row(self):
        return self.data.copy()


class Reference(object):

    def __init__(self, cube, data, type_):
        self.cube = cube
        data['name'] = data['name'].lower()
        self.data = data
        self.type_ = type_

    @property
    def name(self):
        return self.data.get('name')

    @property
    def data_type(self):
        return self.data.get('data_type')

    def to_row(self):
        d = self.to_dict()
        del d['name']
        d['dimension_name'] = self.name
        d['cube_name'] = self.cube.name
        return d

    def to_dict(self):
        d = self.data.copy()
        d['type'] = self.type_
        return d


class Cube(object):

    def __init__(self, name, data):
        self.name = name.lower()
        self.provenance, self.data = data.split('\n', 1)

    @property
    def sections(self):
        if not hasattr(self, '_sections'):
            sections = defaultdict(list)
            section = None
            for row in self.data.split('\n'):
                if row.startswith('K;'):
                    _, section, _ = row.split(';', 2)
                sections[section].append(row)

            self._sections = {}
            for name, rows in sections.items():
                self._sections[name] = Section(rows)

        return self._sections

    @property
    def metadata(self):
        if not hasattr(self, '_metadata'):
            md = {
                'name': self.name,
                'provenance': self.provenance,
                'statistic': self.sections['ERH'].first,
                'cube': self.sections['DQ'].first,
                'units': list(self.sections['ME'])
                }
            md['statistic'].update(self.sections['ERH-D'].first)
            md['cube'].update(self.sections['DQ-ERH'].first)
            md['cube']['statistic_name'] = md['cube']['key'].lower()
            del md['cube']['key']
            md['statistic']['name'] = md['statistic']['key'].lower()
            del md['statistic']['key']
            self._metadata = md
        return self._metadata

    @property
    def dimensions(self):
        if not hasattr(self, '_dimensions'):
            self._dimensions = {}
            for dim in self.sections['MM']:
                self._dimensions[dim['name'].lower()] = Dimension(self, dim)
            values = {}
            for val in self.sections['KMA']:
                values[val['key']] = val
            for assoc in self.sections['KMAZ']:
                self._dimensions[assoc['name'].lower()].add_value(values[assoc['key']], assoc)
        return self._dimensions

    @property
    def axes(self):
        if not hasattr(self, '_axes'):
            self._axes = [Reference(self, a, 'axis') for a in self.sections['DQA']]
        return self._axes

    @property
    def times(self):
        if not hasattr(self, '_times'):
            self._times = [Reference(self, a, 'time') for a in self.sections['DQZ']]
        return self._times

    @property
    def measures(self):
        if not hasattr(self, '_measures'):
            self._measures = [Reference(self, a, 'measure') for a in self.sections['DQI']]
        return self._measures

    @property
    def references(self):
        return self.axes + self.times + self.measures

    @property
    def facts(self):
        if not hasattr(self, '_facts'):
            self._facts = []
            for row in self.sections['QEI'].rows:
                self._facts.append(Fact(self, row))
        return self._facts

    def to_dict(self):
        return {
            'metadata': self.metadata,
            'dimensions': self.dimensions,
            'facts': self.facts
            }

    def to_row(self):
        d = self.metadata.get('cube').copy()
        d['name'] = self.name
        d['provenance'] = self.provenance
        return d

    def __repr__(self):
        return self.provenance


