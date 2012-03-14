
from tabby.base import OBJECT, DICT

class Struct(object):
	def __init__(self, data):
		for k, v in data:
			setattr(self, k, v)

	def pop(self, arg, default=None):
		return self.__dict__.pop(arg, default)

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
			raise fields.TabbyError('Missing column `%s`.' % field.column)

	rows = (row for row in data if len(row) > 0)

	if format == DICT:
		return iter_dicts(rows, field_map)
						
	elif format == OBJECT:
		return iter_objects(rows, field_map)

	else:
		raise TabbyError('Invalid format: %s' % format)

def iter_dicts(rows, field_map):
	for row in rows:
		r = ((field.name, field.default if i is None else field.parse(row[i])) for field, i in field_map)
		yield dict(r)

def iter_objects(rows, field_map):
	for row in rows:
		o = ((field.name, field.default if i is None else field.parse(row[i])) for field, i in field_map)
		yield Struct(o)

def get_cell(row, field, col):
	return field.default if col is None else field.parse(row[col])