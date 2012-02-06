import sys
import ipfix_msg
import templateregistry
def parse(fd):
	tr = templateregistry.templateregistry()
	message = ipfix_msg.ipfix_msg(fd, tr) #Will pop one ipfix message off the stack
	message = ipfix_msg.ipfix_msg(fd, tr) #Will pop one ipfix message off the stack

if __name__ == "__main__":
	filename = sys.argv[1] 
	fd = file(filename)
	parse(fd)
