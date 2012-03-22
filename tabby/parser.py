
from tabby.base import OBJECT, DICT, NAMEDTUPLE, Obj, TabbyError

def parse(fields, data, cols=None, format=DICT, use_cache=False):
    # if cols were not supplied use the first item in data
    data = iter(data)
    if cols is None:
        cols = data.next()
        cols = [c.strip() for c in cols]

    # create a mapping of cols to row indicees
    col_map = dict((col, i) for i, col in enumerate(cols))

    missing_fields, included_fields = build_fields(fields, col_map)        

    # filter out empty rows
    rows = (row for row in data if len(row) > 0)

    iter_encoder = get_encoder(format)

    return iter_encoder(rows, missing_fields, included_fields, use_cache)

def build_fields(fields, col_map):

    missing_fields = []
    included_fields = []

    for field in fields:
        index = col_map.get(field.column)
        if index is None:

            if field.required:
                raise TabbyError('Missing column `%s`.' % field.column)

            missing_fields.append((field.name, field.default))
        else:
            included_fields.append((index, field.name, field.parse))

    return tuple(missing_fields), tuple(included_fields)

def get_encoder(format):
    if format == DICT:
        return iter_dicts

    elif format == OBJECT:
        return iter_objects

    elif format == NAMEDTUPLE:
        return iter_namedtuples

    raise TabbyError('Invalid format: %s' % format)

def iter_dicts(rows, missing_fields, included_fields, use_cache):
    for row in rows:
        s = dict(missing_fields)
        s.update((name, parser(row[i])) for i, name, parser in included_fields)
        
        yield s

def iter_objects(rows, missing_fields, included_fields, use_cache):

    cache = {}

    for row in rows:
        s = Obj()

        for name, value in missing_fields:
            setattr(s, name, value)

        if use_cache:
            for i, name, f_parse in included_fields:
                orig_value = row[i]
                key = (f_parse, orig_value)

                try:
                    value = cache[key]
                except KeyError:
                    value = f_parse(orig_value)
                    cache[key] = value

                setattr(s, name, value)
        else:
            for i, name, f_parse in included_fields:
                setattr(s, name, f_parse(row[i]))
        
        yield s


def iter_namedtuples(rows, missing_fields, included_fields, use_cache):
    from collections import namedtuple

    field_names = tuple(name for _, name, _ in included_fields)

    NamedTuple = namedtuple('NamedTuple', field_names)

    for f_name, f_default in missing_fields:
        setattr(NamedTuple, f_name, f_default)

    # remove name, we don't need it anymore
    included_fields = tuple((i, f_parse) for i, _, f_parse in included_fields)

    maker = NamedTuple._make
    for row in rows:
        yield maker(tuple(f_parse(row[i]) for i, f_parse in included_fields))
