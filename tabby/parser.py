def parse(fields, data, cols=None):
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

	for row in data:
		if len(row) == 0:
			continue

		result = ((field.name, field.default if i is None else field.parse(row[i])) for field, i in field_map)
		result = dict(result)
		

		yield result

	

