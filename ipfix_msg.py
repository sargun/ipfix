try:
	import cStringIO as StringIO
except ImportError:
	import StringIO
import struct, operator
import ipfix_set
#Python's Binary format sucks.
HEADER_FORMAT = "!HHIII"
DEBUG = True
#ipfix_message
class ipfix_msg:
	def __init__(self, fd, templateregistry):
		self.templateregistry = templateregistry
		self.readHeader(fd)
		self.buffer = fd.read(self.Length - struct.calcsize(HEADER_FORMAT))
		fd = StringIO.StringIO(self.buffer)
		self.parseSets(fd)
	def readHeader(self, fd):
		HeaderBin = fd.read(struct.calcsize(HEADER_FORMAT))
		if DEBUG: self.HeaderBin = HeaderBin
		self.VersionNumber, \
			self.Length, \
			self.ExportTimeSecs, \
			self.SeqNumber, \
			self.ObsDomID = struct.unpack(HEADER_FORMAT, HeaderBin)
		self.MesgLength = self.Length - struct.calcsize(HEADER_FORMAT)
		
#		self.parseSets(fd)
		
	def parseSets(self, fd):
		self.sets = []
		while reduce(operator.add, map((lambda x: x.Length), self.sets), 0) < self.MesgLength:
			if DEBUG: print "Making set"
			Set = ipfix_set.ipfix_set(self, fd, self.templateregistry)
			self.sets.append(Set)

