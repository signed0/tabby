from tabby.fields import Field
from tabby.parser import parse

class SchemaMeta(type):
    '''The metaclass for a validator. Takes a class definition and adds a
       validate method based off of the fields defined, while removing the 
       attributes that map to fields.'''

    def __new__(cls, name, parents, _attrs):

        attrs = dict()
        fields = []

        # iterate through the attributes in the class definition
        for key, value in _attrs.iteritems():

            if isinstance(value, Field):
                # set the name of the field, based on its name in the class
                # definition
                value.set_name(key)

                # add the field to the list of Fields
                fields.append(value)

            else:
                # it is not a field, include it in the new class definition
                attrs[key] = value

        attrs['fields'] = fields

        return super(SchemaMeta, cls).__new__(cls, name, parents, attrs)

class Schema(object):
    '''A object that all validators need to subclass'''

    __metaclass__ = SchemaMeta

    @classmethod
    def process(cls, *args, **kwargs):
        return parse(cls.fields, *args, **kwargs)
