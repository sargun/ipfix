import struct
import ipfix_field, ipfix_scopefield
HEADER_FORMAT = "!HH"
DEBUG = True

class ipfix_record:
	def __init__(self, Set, fd, templateregistry):
		self.Set = Set
		self.templateregistry = templateregistry
		self.readHeader(fd)
		self.readFields(fd)
		if self.__class__.__name__ in ['ipfix_templaterecord', 'ipfix_optionrecord']:
			self.templateregistry.register(self, self.TemplateID)
			self.setup_realtemplate()
	def readHeader(self, fd):
		HeaderBin = fd.read(struct.calcsize(HEADER_FORMAT))
		self.TemplateID, \
		self.FieldCount = struct.unpack(HEADER_FORMAT, HeaderBin)
	def readFields(self, fd):
		self.fields = []
		for n in xrange(self.FieldCount):
			self.fields.append(ipfix_field.ipfix_field(self, fd))
