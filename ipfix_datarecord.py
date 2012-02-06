import struct
import ipfix_record
HEADER_FORMAT="!HH"

class ipfix_datarecord(ipfix_record.ipfix_record):
	def readHeader(self, fd):
#		HeaderBin = fd.read(struct.calcsize(HEADER_FORMAT))
#		self.TemplateID, \
#		self.Length = struct.unpack(HEADER_FORMAT, HeaderBin)
		#Data records don't have shit.
		pass 
	def readFields(self, fd):
#		print self.templateregistry.templates
		Template =  self.templateregistry.templates[self.Set.SetID]
		RealTemplate = Template.get_realtemplate()
		RealTemplate.populate(fd)
		print "Reading fields for template id: %s, Template: %s" % (self.Set.SetID, Template)
		raise Exception("not implemented")

