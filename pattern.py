#!/usr/bin/env python
#A decent made pattern_create && pattern_offset
#by Tomasuh @ tomasuh.github.io
import sys, re, argparse
fn =  sys.argv[0]

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='A working pattern_create and pattern_offset script!', 
	epilog = 'Example usages:\n'+ fn + ' -pc 100, to generate a pattern of 100 bytes with default sets.\n'
	+ fn + ' -pc 20 -s1 ALFA -s2 BI -s3 3, to generate a pattern of 20 bytes with given sets.\n'
	+ fn + ' -pc 100 -po c9Ad, to match on a pattern of 100 bytes with given key, you can do same with given sets.\n'
	+ fn + ' -pc 20 -bc AB, will generate a pattern without A and B\n'
	+ fn + ' -pc 20 -pc 20 -po 0x5AAa -hl will search for the offset to the key that\'s in little endian format, -hb for big endian.\n'
	)
parser.add_argument('-pc', dest='pattern_create', help="Generate pattern of given size", type=int, required = True)
parser.add_argument('-s1', '--set1', dest='set1', help="set1 characters", default = "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
parser.add_argument('-s2', '--set2', dest='set2', help="set1 characters", default = "abcdefghijklmnopqrstuvwxyz")
parser.add_argument('-s3', '--set3', dest='set3', help="set1 characters", default = "0123456789")
parser.add_argument('-bc', '--bad_chars', dest='bad_chars', help="Chars to exclude from generated pattern", default = "")
parser.add_argument('-po', '--pattern_offset', dest='pattern_offset', help="Find offset for given key", type=str, required=False)
parser.add_argument('-hl', '--hex_little_endian', dest='hex_little_endian', help="If given key to search are in little endian format 0xXXXX arbitrary length. Accepts without starting 0x also.", action="store_true")
parser.add_argument('-hb', '--hex_big_endian', dest='hex_big_endian', help="If given key to search are in big endian format 0xXXXX arbitrary length. Accepts without starting 0x also.", action="store_true")

args = parser.parse_args()

set1 = args.set1
set2 = args.set2
set3 = args.set3


def removeBadChars(inputStr):
	return ''.join(i for i in inputStr if i not in args.bad_chars)

#Recursive looks so good :)
def reverseHexOrder(aHexStr):
	if len(aHexStr) == 2:
		return aHexStr
	else:
		return reverseHexOrder(aHexStr[2:]) + aHexStr[0:2]

set1 = removeBadChars(set1)
set2 = removeBadChars(set2)
set3 = removeBadChars(set3)

def pattern_create(size):
	count = 0
	outp = ""
	for chars1 in set1:
		for chars2 in set2:
			for chars3 in set3:
				outp += chars1+chars2+chars3
				count+=3
				if count == size:
					return outp	
				if count>=size:
					break
			if count>=size:
				break
		if count>=size:
			break

	#Because of the for loop adding 3 chars each time its appending to outp we eventually may need to remove some.
	while(size <= len(outp)):
		outp=outp[:-1]
		size+=1

	return outp

def pattern_offset(key,size):
	pattern = pattern_create(size)

	if args.hex_little_endian or args.hex_big_endian:
		if key[0:2] == "0x":
			key = key[2:]
		if args.hex_little_endian: # reverse order
			key = reverseHexOrder(key)
		key = key.decode("hex")

	res = re.search(key,pattern)
	if res:
		return res.start()


if args.pattern_create and not args.pattern_offset:
	print pattern_create(args.pattern_create)

elif args.pattern_create and args.pattern_offset:
	res = pattern_offset(args.pattern_offset, args.pattern_create)
	if res:
		print "Offset to pattern:" ,res
	else:
		print "No match..."