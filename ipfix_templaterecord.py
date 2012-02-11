import struct
import ipfix_record
import ipfix_field, ipfix_scopefield
HEADER_FORMAT = "!HH"
DEBUG = True

class ipfix_templaterecord(ipfix_record.ipfix_record):
	pass

#class ipfix_templaterecord:
#	def __init__(self, Set, fd, templateregistry):
#		self.Set = Set
#		self.templateregistry = templateregistry
#		self.readHeader(fd)
#		self.readFields(fd)
#		self.templateregistry.register(self, self.TemplateID)
class ipfix_templaterecord(ipfix_record.ipfix_record):
	def readHeader(self, fd):
		HeaderBin = fd.read(struct.calcsize(HEADER_FORMAT))
		self.TemplateID, \
		self.FieldCount = struct.unpack(HEADER_FORMAT, HeaderBin)

	def readFields(self, fd):
		self.fields = []
		for n in xrange(self.FieldCount):
			self.fields.append(ipfix_field.ipfix_field(self, fd))
	def setup_realtemplate(self):
		pass
#		self.ipfix_realtemplate.fields = self.fields 
	def get_realtemplate(self):
		realtemplate = self.ipfix_realtemplate()
		for i in self.fields:
			realtemplate.fields.append(i.get_realfield())
		return realtemplate
	class ipfix_realtemplate:
		fields = []
		values = {}
		def populate(self, fd):
			for i in self.fields:
				print "Setting field: %s" % i
				if i==None: continue
				i.readField(self, fd)
				self.values[i.name] = i
				setattr(self, i.name, i)
			print "Populated values: %s" % (self.values)
