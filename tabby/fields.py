import logging
from datetime import date, time

from tabby.base import TabbyError

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

    def default_or_error(self):
        '''Returns the default or throw an exception if this field is requried'''
        if self.required:
            raise TabbyError('%s is a required field' % self.name)
        else:
            return self.default

    def parse(self, value):
        if value is '':
            value = None
        else:
            value = value.strip()
            if value is '':
                value = None

        if value is None:
            if self.required:
                raise TabbyError('%s is a required field' % self.name)
            else:
                return self.default

        try:
            return self.coerce(value)

        except ValueError, e:
            
            logging.warning(e)
            raise TabbyError('Unable to parse value for %s, (%s)' % (self.name, value))

class _NumberField(Field):

    def parse(self, value):
        if value is '':
            if self.required:
                raise TabbyError('%s is a required field' % self.name)
            else:
                return self.default

        try:
            return self.coercer(value)
        except ValueError, e:
            if value.isspace():
                return self.default_or_error()

            logging.warning(e)
            raise TabbyError('Unable to parse value for %s, (%s)' % (self.name, value))


class StringField(Field):

    def parse(self, value):
        if value is '':
            value = None
        else:
            value = value.strip()
            if value is '':
                value = None

        if value is None:
            if self.required:
                raise TabbyError('%s is a required field' % self.name)
            else:
                return self.default

        return value

class BoolField(Field):
    def coerce(self, value):
        if value.lower() in ('0', 'false', 'f'):
            return False

        return True

class IntField(_NumberField):
    coercer = int

class FloatField(_NumberField):
    coercer = float

class TimeField(Field):
    def coerce(self, value):
        h, m, s = [int(i) for i in value.split(':')]
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

