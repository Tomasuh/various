import zipfile,sys,argparse,pprint,pickle,thread,threading, Queue

parser = argparse.ArgumentParser(description='Commandline options zip extractor')
parser.add_argument('-s', '--saved-logfile', dest='savedLogfile', help="Saved logfile to continue work from")
parser.add_argument('-l', '--logfile', dest='logfile', help="Logfile to save to if --saved-logfile is not used")
parser.add_argument('-f', '--file', dest='file', help="ZIP file to read from.")
parser.add_argument('-p', '--password', dest='password', help="Password to zip", default=None)
parser.add_argument('-d', '--extract-dir', dest='dir', help="Directory to extract files to.", default=".")
parser.add_argument('-b', '--backup-count', type=int, default=100, dest='backup', help="How often save position in extraction, int.")
parser.add_argument('-q', '--quit-at', type=int, dest='quit', help="Quit extracting after given number of files have been extracted")
parser.add_argument('-t', '--threads', type=int, default=10, dest='thread', help="Number of threads")

args = parser.parse_args()

if not (args.logfile or args.savedLogfile):
	parser.error('A log file must be specified') 

if not (args.file):
	parser.error('A zip file must be specified') 

class readZip(object):
	"""docstring for readZip"""
	def __init__(self):
		queue = Queue.Queue() # for return value from thread
		lock = threading.Lock()
		counter=0
		global archive
		archive = zipfile.ZipFile(args.file)
		archive.setpassword(args.password)
		fileList = []
		if (args.logfile):
			fileList=archive.namelist()
			self.writeObject(fileList,args.logfile)
		else:
			fileList=self.readObject(args.savedLogfile)
			args.logfile=args.savedLogfile# for simplicity later on


		threadList=[]
		for a in range (args.thread):
			t = threading.Thread(target=self.looper, args=(archive,fileList, queue))
			t.start()
			threadList.append(t)

		for thread in threadList:
			thread.join()
		self.writeObject(queue.get(),args.logfile)

	def looper(self,a,f, queue):
		global archive
		archive = a
		global fileList
		fileList=f
		global counter
		counter=0
		lock = threading.RLock()

		while fileList!=[]:
			fileName = fileList.pop()
			print "Extracted: "+ fileName
			archive.extract(fileName,args.dir)
			if(args.quit and args.quit == counter):
				queue.put(fileList)
				return
			counter+=1

	def writeObject(self,theList, filename):
		with open(filename, 'wb') as output:
			pickle.dump(theList, output, pickle.HIGHEST_PROTOCOL)

	def readObject (self,filename):
		with open (filename,'rb') as readFile:
			return pickle.load(readFile)


readZip()

