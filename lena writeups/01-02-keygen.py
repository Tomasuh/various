f = open("Keyfile.dat","w")
nrOfNeededG = 8
nrOfNeededChars = 16
key = nrOfNeededG * 'G'
key += (nrOfNeededChars - nrOfNeededG) * 'E'
f.write(key)
f.close()
