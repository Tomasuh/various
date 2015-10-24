import random,sys

random.seed()

sys.argv[1] = sys.argv[1].replace('x','')
sys.argv[1] = sys.argv[1].replace('\\','')
shellcode = bytearray(sys.argv[1].decode('hex'))

#Randomized value to xor byte with
def randXOR():
	return random.randint(1,255)

encoded = ""

encoded2 = ""

for byte in shellcode:
	#We dont want an encoded byte resulting in null
	randVal = randXOR()
	while (randVal^byte) == 0:
		randVal = randXOR()

	print "Byte is: %x \txor \t with:%d \t encoded value: %x" % (byte,randVal,byte^randVal)
	byte ^= randVal #XOR byte with randomized randVal

	#PY version
	#First XOR'd byte from shellcode
	encoded += '\\x'
	encoded += '%02x' % byte
	
	#Second value is randomized XOR value to restore byte
	encoded += '\\x'
	encoded += '%02x' % randVal

	encoded2+= '0x%02x,' % byte
	encoded2+= '0x%02x,' % randVal

print "\nGiven shellcode size (bytes): %d\nOutput shellcode size (bytes): %d\n" % (len(shellcode),len(encoded)/4)

print "Generated shellcode python/c style:"
print encoded+"\n"
print "Generated shellcode nasm style:"
print encoded2
