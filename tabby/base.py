
NAMEDTUPLE = 'namedtuple'
DICT = 'dict'
OBJECT = 'object'

class TabbyError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class Obj():
    pass

class Struct(object):

    def __init__(self, data=None, **kwargs):
        '''Instantiates an object using either a single dictionary or keyword 
        arguments
        '''

        self.__dict__ = data or kwargs
