import struct, types

HEADER_FORMAT = "!HH"
PEN_FORMAT="!I"
DEBUG = True
PEN_BIT = (0x1 << 15)

class ipfix_field:
	def __init__(self, Template, fd):
		self.Template = Template
		self.readHeader(fd)
		self.setup_realfield()
	def readHeader(self, fd):
		HeaderBin = fd.read(struct.calcsize(HEADER_FORMAT))
		self.InformationElementID, \
                self.FieldLength = struct.unpack(HEADER_FORMAT, HeaderBin)
		if self.FieldLength == 65535:
			self.variableLength = True
			self.FieldLength = -1
		else:
			self.variableLength = False

		self.HasPEN = (PEN_BIT & self.InformationElementID) == PEN_BIT
		#Cheating, 0xFFFF should be dynamic based on the size of the PEN, probably 2**sizeof(PEN*8)-1
		SIZEOF_PEN_BITS = struct.calcsize(PEN_FORMAT) * 8
		self.InformationElementID = ((2**SIZEOF_PEN_BITS-1) - PEN_BIT) & self.InformationElementID
		if DEBUG: print "Information Element ID: %s" % (self.InformationElementID)
		if DEBUG: print "Reading Template ID: %s" % (self.Template.TemplateID)
		if self.HasPEN:
			PENBin = fd.read(struct.calcsize(PEN_FORMAT))
			self.PEN = struct.unpack(PEN_FORMAT, PENBin)
			print "PEN: %s" % (self.PEN)

		else:
			self.PEN = None
	def setup_realfield(self):
		pass
	def get_realfield(self):
		realfield = self.ipfix_realfield()
		realfield.InformationElementID = self.InformationElementID
		realfield.FieldLength = self.FieldLength
		realfield.PEN = self.PEN
		return realfield
	class ipfix_realfield:
		def __repr__(self):
			return '<ipfix_realfield, ID: %s>' % (self.InformationElementID)
			
