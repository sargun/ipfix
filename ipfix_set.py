import struct
import ipfix_templaterecord

HEADER_FORMAT = "!HH"
DEBUG = True
class UndefinedSetException(Exception): pass
class ipfix_set:
	def __init__(self, Mesg, fd):
		self.Mesg = Mesg
		self.readHeader(fd)
	def readHeader(self, fd):
		HeaderBin = fd.read(struct.calcsize(HEADER_FORMAT))
		if DEBUG: self.HeaderBin = HeaderBin
		self.SetID, \
		self.Length = struct.unpack(HEADER_FORMAT, HeaderBin)
		self.SetLength = self.Length - struct.calcsize(HEADER_FORMAT)
		if self.SetID == 2:
			self.set_type = "template"
			self.record_type = ipfix_templaterecord.ipfix_templaterecord
		elif self.SetID == 3:
			self.set_type = "option"
		elif (self.SetID > 3 and self.SetID < 256) or (self.SetID < 2):
			raise UndefinedSetException("ID: %s" % (self.SetID))
		else:
			self.set_type = "data"
		self.parseRecords(fd)

	def parseRecords(self, fd):
		self.records = []
		self.data_records = []
		self.option_records = []
		if DEBUG: print "Parsing set ID: %s" % (self.SetID)
		#TODO IMPLEMENT loop.
		self.records.append(self.record_type(self, fd))
