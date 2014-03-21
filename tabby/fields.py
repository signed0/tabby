import datetime, re
from decimal import Decimal

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
            raise TabbyError('{} is a required field.'.format(self.name))
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
                raise TabbyError('{} is a required field.'.format(self.name))
            else:
                return self.default

        try:
            return self.coerce(value)

        except ValueError as e:
            raise TabbyError('Unable to parse value for {}, {}: {}'.format(self.name, value, e))

class _NumberField(Field):

    def parse(self, value):
        if value is '':
            if self.required:
                raise TabbyError('{} is a required field.'.format(self.name))
            else:
                return self.default

        try:
            return self.coercer(value)
        except ValueError as e:
            if value.isspace():
                return self.default_or_error()

            raise TabbyError('Unable to parse value for {}, {}: {}.'.format(self.name, value, e))

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
                raise TabbyError('{} is a required field.'.format(self.name))
            else:
                return self.default

        return value
        
class UnicodeField(Field):

    def parse(self, value):
        value = value.strip()
        
        if value is '':
            if self.required:
                raise TabbyError('{} is a required field.'.format(self.name))
            else:
                return self.default

        return value.decode('UTF-8')

class BoolField(Field):

    def coerce(self, value):
        if value.lower().decode('UTF-8') in ('0', 'false', 'f'):
            return False

        return True

class IntField(_NumberField):
    coercer = int

class FloatField(_NumberField):
    coercer = float

class DecimalField(_NumberField):

    def coercer(self, value):
        v = value.strip().decode('UTF-8')
        
        if not v:
            if self.required:
                raise TabbyError('{} is a required field.'.format(self.name))
            else:
                return self.default

        try:
            return Decimal(v)
        except Exception as e:
            raise TabbyError('Unable to parse value for {}, {}: {}.'.format(self.name, value, e))

class DateTimeField(Field):

    DEFAULT_FMT = '%Y-%m-%dT%H:%M:%S'

    def __init__(self, *args, **kwargs):
        self.fmt = kwargs.pop('fmt', self.DEFAULT_FMT)

        Field.__init__(self, *args, **kwargs)

    def coerce(self, value):
        return datetime.datetime.strptime(value.decode('UTF-8'), self.fmt)

class DateField(DateTimeField):
    
    DEFAULT_FMT = '%Y-%m-%d'

    def coerce(self, value):
        return datetime.datetime.strptime(value.decode('UTF-8'), self.fmt).date()

class TimeField(DateTimeField):

    DEFAULT_FMT = '%H:%M:%S'

    def coerce(self, value):
        return datetime.datetime.strptime(value.decode('UTF-8'), self.fmt).time()

class HumanTimespanField(Field):

    def parse(self, value):
        value = value.strip().decode('UTF-8')
        
        if not value:
            if self.required:
                raise TabbyError('{} is a required field.'.format(self.name))
            else:
                return self.default

        match = re.match(r'(\d+) hours? [a-z ]*(\d+) min', value)
        if match:
            hours, minutes = match.groups()
            return int(hours) * 3600 + int(minutes) * 60

        match = re.match(r'(\d+) hours?', value)
        if match:
            hours, = match.groups()
            return int(hours) * 3600

        match = re.match(r'(\d+) min', value)
        if match:
            minutes,  = match.groups()
            return int(minutes) * 60

        if self.required:
            raise TabbyError('{} is a required field.'.format(self.name))
        else:
            return self.default

class ColorField(Field):

    def coerce(self, value):
        v = value.lower().strip().decode('UTF-8')

        if not v:
            if self.required:
                raise TabbyError('{} is a required field.'.format(self.name))
            else:
                return self.default

        if not re.match(r'^[0-9a-f]+$', v):
            raise TabbyError('Incorrect color format: "{}".'.format(value))

        if len(v) == 3:
            v = ''.join((v[0], v[0], v[1], v[1], v[2], v[2]))

        if not len(v) == 6:
            raise TabbyError('Incorrect color format: "{}".'.format(value))
        
        return v

