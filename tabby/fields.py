import logging
from datetime import date, time

class TabbyError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

def str_or_none(value):
    if len(value) == 0:
        return None

    value = value.strip()

    if len(value) == 0:
        return None

    return value

class Field(object):
    def __init__(self, column=None, default=None, required=False, name=None):
        # name is what the field will be stored as
        # column is the name used in the incoming data

        self.name = column if name is None else name
        self.column = column
        self.default = default
        self.required = required

    def set_name(self, value):
        self.name = value
        if self.column is None:
            self.column = value

    def parse(self, value):
        value = str_or_none(value)
        if value is None:
            if self.required:
                raise TabbyError('%s is a required field' % self.name)
            else:
                return self.default

        try:
            return self.coerce(value)
        except Exception, e:
            logging.warning(e)
            raise TabbyError('Unable to parse value for %s, (%s)' % (self.name, value))

class StringField(Field):

    def coerce(self, value):
        return value

class BoolField(Field):
    def coerce(self, value):
        if value.lower() in ('0', 'false', 'no', 'f', 'n'):
            return False

        return True

class IntField(Field):
    def coerce(self, value):
        return int(value)

class FloatField(Field):
    def coerce(self, value):
        return float(value)

class TimeField(Field):
    def coerce(self, value):
        value = value.split(':')
        h, m, s = value
        return time(h, m, s)

class DateField(Field):
    def coerce(self, value):
        year = int(value[:4])
        month = int(value[4:6])
        day = int(value[6:])

        return date(year, month, day)

class ColorField(Field):

    def coerce(self, value):
        value = value.upper()
        
        if not len(value) == 6:
            return self.default
        
        return value

