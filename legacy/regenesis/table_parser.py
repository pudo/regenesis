import math
from pprint import pprint
from datetime import datetime
from itertools import repeat, izip_longest
import variable

# STATES
META = 1
HEADER = 2
DATA = 3
NOTICES = 4

class tableParser(object):
    
    def __init__(self, structure, variables, csv_data):
        self.structure = structure
        self.csv_data = csv_data
        self.notices = []
        
        # lookup of all variables in this table
        self.variables = dict([(v, variable.get(v)) for v in variables])
        
        # global variables are common to all cells
        global_variables = [k for k, v in structure['global']][::-1]
        self.statistic_id = global_variables.pop()
        self.global_variables = global_variables[::-1]
        
        # columns variables are partially indented
        self.indented_columns = {}
        for var, level in structure['top']:
            self.indented_columns[level] = self.indented_columns.get(level, []) + [var]
                        
        # row variables are common to each cell in a row
        self.num_row_variables = None
        self.row_variables = [k for k, v in structure['pre']]
        self.row_id = 0
        
        # column headers combine general information that is true for all
        # columns
        self.column_headers = []
        self.column_headers_parsed = False
        self.column_data = {}
        self.column_types = None
        self.column_units = None
        
        # the actual results
        self.cells = []
        self.current_row_data = None
        
                
    def handle_notice(self, line):
        self.notices.append(line)
    
        
    def handle_meta(self, columns):
        pass # discard this
    
        
    def handle_header(self, columns):
        if self.num_row_variables is None:
            self.num_row_variables = len([c for c in columns if not len(c)])
        columns = columns[self.num_row_variables:]
        self.num_row_columns = len(columns)
        self.column_headers.append(columns)
    
    
    def _types(self, variables):
        return [self.variables.get(v, {}).get('typ', '') for v in variables]
        
    def _names(self, variables):
        return [self.variables.get(v, {}).get('inhalt', '') for v in variables]
        
    def parse_column_headers(self):
        # column variables describe the values in each column
        column_variables = []
        pprint(self.indented_columns)
        for level in self.indented_columns.values():
            level = level * (self.num_row_columns/len(level))
            assert len(level) == self.num_row_columns, [level, self.num_row_columns]
            column_variables.append(level)
        column_variables = column_variables[::-1]
        
        #print "HUHU " + "*" * 100
        #print self.global_variables
        #print "HUHU " + "*" * 100
        
        self.column_data = {}
        next_variables = None
        for header in self.column_headers:
            assert len(header) == self.num_row_columns
            
            if next_variables is None:
                if len(column_variables):
                    next_variables = column_variables.pop()
                else:
                    # this should happen once at most:
                    next_variables = [self.global_variables.pop()] * self.num_row_columns
            
            if header == self._names(next_variables):
                continue # skip type description header rows
            
            types = self._types(next_variables)
            if u'Wert' in types:
                # TODO: units are always the last entry. maybe check this? 
                self.column_units = header
                self.column_types = next_variables
            else:
                for i, (var, val) in enumerate(zip(next_variables, header)):
                    data = self.column_data.get(i, {})
                    data[var] = val
                    self.column_data[i] = data
            
            next_variables = None 
        
        # make sure we have a cell type set for all columns:
        if self.column_types is None:
            self.column_types = [self.global_variables.pop()] * self.num_row_columns
        
        #print "HAHA " + "*" * 100
        #print self.column_types
        #print "HAHA " + "*" * 100
        
        self.column_headers_parsed = True
    
    
    def parse_row_headers(self, headers):
        if len(self.row_variables) == 1 and len(headers) > 1:
            self.current_row_data = {self.row_variables[0]: headers}
            return
        
        if len(headers) < len(self.row_variables):
            _headers = []
            for header in headers:
                if '/' in header:
                    _headers.extend(header.split('/', 1))
                else:
                    _headers.append(header)
            headers = _headers
        
        self.current_row_data = {}
        for var, hdr in izip_longest(self.row_variables, headers):
            if var == 'SMONAT':
                if '/' in hdr:
                    hdr, _next = hdr.split('/', 1)
                    headers.append(_next)
                elif len(hdr) > 2:
                    headers.append(hdr)
                    hdr = None
            self.current_row_data[var] = hdr
        
        assert len(self.current_row_data.items()) == len(headers), self.current_row_data
        #self.current_row_data = dict(zip(self.row_variables, headers))
        
    
    def create_cell(self, column_idx, value):
        cell = {self.column_types[column_idx]: value,
                '__key': self.column_types[column_idx],
                '__partOf': self.global_variables,
                '__statId': self.statistic_id,
                '__cellId': '#' + str(self.row_id) + ":" + str(column_idx)}
        cell.update(self.current_row_data)
        cell.update(self.column_data.get(column_idx, {}))
        if self.column_units:
            cell['__unit'] = self.column_units[column_idx]
        self.cells.append(cell)
    
    
    def handle_data(self, columns):
        self.row_id += 1
        if not self.column_headers_parsed:
            self.parse_column_headers()
        self.parse_row_headers(columns[:self.num_row_variables])
        columns = columns[self.num_row_variables:]
        for column_idx, value in enumerate(columns):
            self.create_cell(column_idx, value)
        
    
    def parse(self):
        state = META
        for no, line in enumerate(self.csv_data.split('\r\n')):
            line = line.strip()
            if no == 0: continue
            if line.startswith("___") and not ';' in line: 
                if state == DATA:
                    state = NOTICES
                    continue
            if state == NOTICES and len(line):
                self.handle_notice(line)
            entries = line.split(';')
            if state == META:
                if not len(entries[0]):
                    state = HEADER
                else: self.handle_meta(entries)
            if state == HEADER:
                if len(entries[0]):
                    state = DATA
                else: self.handle_header(entries)
            if state == DATA:
                self.handle_data(entries)
    
    def to_dict(self):
        #pprint(self.cells)
        return {'notices': '\n'.join(self.notices),
                'cells': self.cells}
                
