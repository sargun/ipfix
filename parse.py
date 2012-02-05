import sys
import ipfix_msg
def parse(fd):
	message = ipfix_msg.ipfix_msg(fd) #Will pop one ipfix message off the stack

if __name__ == "__main__":
	filename = sys.argv[1] 
	fd = file(filename)
	parse(fd)
