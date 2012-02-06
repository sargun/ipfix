import struct
#import ipfix_templaterecord
import ipfix_record
import ipfix_field, ipfix_scopefield
DEBUG = True
HEADER_FORMAT = "!HHH"

class ipfix_optionrecord(ipfix_record.ipfix_record):
	def readHeader(self, fd):
		HeaderBin = fd.read(struct.calcsize(HEADER_FORMAT))
		self.TemplateID, \
		self.FieldCount, \
		self.ScopeFieldCount = struct.unpack(HEADER_FORMAT, HeaderBin)
	def readFields(self, fd):
		self.scopefields = []
		self.fields = []
		for n in xrange(self.ScopeFieldCount):
			self.scopefields.append(ipfix_scopefield.ipfix_scopefield(self, fd))
		for n in xrange(self.FieldCount - self.ScopeFieldCount):
			self.fields.append(ipfix_field.ipfix_field(self, fd))
	def setup_realtemplate(self):
		pass
#		self.ipfix_realtemplate.fields = self.fields 
	def get_realtemplate(self):
		realtemplate = self.ipfix_realtemplate()
		for i in self.fields:
			realtemplate.append(i.get_realfield())
	class ipfix_realtemplate:
		fields = []
		pass

