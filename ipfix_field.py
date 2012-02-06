import struct, types
from BeautifulSoup import BeautifulStoneSoup
HEADER_FORMAT = "!HH"
PEN_FORMAT="!I"
DEBUG = True
PEN_BIT = (0x1 << 15)
XML = file("ipfix.xml").read()
UINT_BY_LEN = {1: 'B', 2: 'H', 4: 'I', 8: 'Q'}

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
			self.PEN = struct.unpack(PEN_FORMAT, PENBin)[0]
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
		realfield.ret_type()
		return realfield
	class ipfix_realfield:
		def __init__(self):
			self.name = None
			self.ignore = False
		def __repr__(self):
			return '<ipfix_realfield: "%s", ID: %s>' % (self.name, self.InformationElementID)
		def ret_type(self):
			BSS = BeautifulStoneSoup(XML)
			try:
				record = BSS.find('elementid',text=self.InformationElementID).parent.parent
			except:
#				raise Exception("Could not find data type: %s in the database" % (self.InformationElementID))
				self.ignore = True
				self.datatype = None
				self.name = None
				return 
			self.datatype = str(record.find("datatype").text)
			self.name = str(record.find("name").text)
			if self.PEN == 29305:
				self.name = self.name + 'Reverse'
			elif self.PEN == 6871:
				self.name = self.name + "CERT"
				self.ignore = True
			elif self.PEN:
				raise Exception("Don't know how to parse pen: %s, ID: %s" % (repr(self.PEN), self.InformationElementID))
		def readField(self, realtemplate, fd):
			BinValue = fd.read(self.FieldLength)
			if 1 == 2:
				pass
			if self.datatype == 'dateTimeMilliseconds':
				self.value = struct.unpack('!'+UINT_BY_LEN[self.FieldLength], BinValue)[0]
			else:
				raise Warning("Could not understand datatype: %s" % (self.datatype))
#			if self.datatype == False
#			self.value = 
