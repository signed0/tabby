
from tabby.base import OBJECT, DICT, NAMEDTUPLE, Struct, TabbyError



def parse(fields, data, cols=None, format=DICT):
	# if cols were not supplied use the first item in data
	data = iter(data)
	if cols is None:
		cols = data.next()
		cols = [c.strip() for c in cols]

	# create a mapping of cols to row indicees
	col_map = dict((col, i) for i, col in enumerate(cols))

	field_map = tuple((field, col_map.get(field.column)) for field in fields)

	for field, index in field_map:
		if field.required and index is None:
			raise TabbyError('Missing column `%s`.' % field.column)

	rows = (row for row in data if len(row) > 0)

	if format == DICT:
		return iter_dicts(rows, field_map)					
	elif format == OBJECT:
		return iter_objects(rows, field_map)
	elif format == NAMEDTUPLE:
		return iter_namedtuples(rows, field_map)
	else:
		raise TabbyError('Invalid format: %s' % format)

def iter_dicts(rows, field_map):
	for row in rows:
		yield dict(get_cell(row, field, col) for field, col in field_map)

def iter_objects(rows, field_map):
	for d in iter_dicts(rows, field_map):
		yield Struct(d)

def iter_namedtuples(rows, field_map):
	from collections import namedtuple

	field_names = tuple(field.name for field , _ in field_map)

	NamedTuple = namedtuple('NamedTuple', field_names)

	for row in rows:
		row = tuple(f.default if i is None else f.parse(row[i]) for f, i in field_map)
		yield NamedTuple._make(row)

def get_cell(row, field, col):
	if col is None:
		return (field.name, field.default)
	else: 
		return (field.name, field.parse(row[col]))