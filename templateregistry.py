DEBUG = False
class templateregistry(object):
	def __init__(self):
		self.templates = {}
	def register(self, Record, TemplateID):
		self.templates[TemplateID] = Record
		if DEBUG: print "Registering Record: %s (%s)" % (repr(Record), TemplateID)
