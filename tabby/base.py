
NAMEDTUPLE = 'namedtuple'
DICT = 'dict'
OBJECT = 'object'

class TabbyError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class Struct(object):
	def __init__(self, data):
		for k, v in data:
			setattr(self, k, v)
