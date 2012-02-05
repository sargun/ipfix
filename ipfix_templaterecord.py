import struct
import ipfix_field
HEADER_FORMAT = "!HH"
DEBUG = True

class ipfix_templaterecord:
	def __init__(self, Set, fd):
		self.Set = Set
		self.readHeader(fd)
	def readHeader(self, fd):
		HeaderBin = fd.read(struct.calcsize(HEADER_FORMAT))
		self.TemplateID, \
		self.FieldCount = struct.unpack(HEADER_FORMAT, HeaderBin)
		self.readFields(fd)
	def readFields(self, fd):
		self.fields = []
		for n in xrange(self.FieldCount):
			self.fields.append(ipfix_field.ipfix_field(self, fd))
