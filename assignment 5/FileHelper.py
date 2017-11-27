# Name: Naveen Venkat
# ID: 2015A7PS0078P

import config

class FileHelper:

	def __init__(self, fileName = None): # Constructor

		self.fileObject = None
		self.fileName = fileName
		self.data = None

		if fileName!= None:
			self.fileObject = open(fileName)


	def __del__(self): # Destructor

		#close file if it is open
		if self.fileObject!= None:
			self.fileObject.close()
	

	def open(self, fileName): # Wrapper to open a file

		self.fileName = fileName
		
		if self.fileObject!=None:
			
			if config.flag_show_warnings:
				print
				print "### WARNING 1 [FileHelper.open()]: self.fileObject is open. fileName =", self.fileName
				print

			self.fileObject.close()

		self.fileObject = open(fileName)
		self.data = None


	def close(self): # Wrapper to close a file

		self.fileName = None
		self.fileObject.close()
		self.fileObject = None


	def readFile(self): # Read the file and put it in self.data

		if self.fileObject == None:
			if config.flag_show_errors:
				print
				print "### FATAL ERROR 1 [FileHelper.readFile()]: self.fileObject is None. Have you opened the file properly?"
				print
			return None

		contents = []

		while(True):
			line = self.fileObject.readline()
			if line=='$$':
				break;
			else:
				line = line.split('\n')[0]
				contents.append(line)
		
		self.data = contents

		return contents


	def parseContents(self): # Parse the contents in self.data
		
		if self.data == None: # No data is present

			if config.flag_show_errors:
				print
				print "### FATAL ERROR 2 [FileHelper.parseContents()]: self.data is None"
				print

			return None

		if type(self.data) == list: # Data may be parsed
			
			if type(self.data[0]) == dict: # If data is already parsed the first item will be a dictionary with a line of data
				
				print
				print "### WARNING 2 [FileHelper.parseContents()]: self.data is already parsed"
				print

				return self.data

			elif type(self.data[0]) == str: # If the first item is a string (raw data from file) parse it
				
				# Creating variables to be used while parsing
				parsedData = []
				splitLine = []
				effectVariable = ""
				causeList = []
				condProbList = []
				priorProb = None
				numCauses = None

				# Parsing each line
				for line in self.data:
					
					splitLine = line.split('>>')

					# Extracting raw data
					effectVariable = splitLine[0].strip()
					priorProb = None
					causeList = splitLine[1].strip()
					numCauses = None
					condProbList = splitLine[2].strip()

					# Building causeList - extracting causes
					causeList = causeList.split('[')[1]
					causeList = causeList.split(']')[0]
					causeList = causeList.split(',')

					for i in range(len(causeList)):
						causeList[i] = causeList[i].strip()

					''' 
					METHOD 1
					Making the causeList as a set
					
					Quoting CPython's documentation:
					"Indeed, CPython's sets are implemented as something like dictionaries with dummy values (the keys 
					being the members of the set), with some optimization(s) that exploit this lack of values"
					
					An O(1) lookup of parents will come in handy in the future
					'''

					# if causeList == ['']:
					# 	causeList = set()

					# causeList = set(causeList)
					

					'''
					METHOD 2
					Keeping causeList as a list and making a set of parents in the Variable Node
					'''
					if causeList == ['']:
						causeList = []

					# Building numCauses - number of causes for the variable
					numCauses = len(causeList)

					# Building condProbList - finding conditional probabilities of the effect given the causes
					condProbList = condProbList.split()

					for i in range(len(condProbList)):
						condProbList[i] = float(condProbList[i].strip())

					# Building priorProb - if there are no causes then the probability given is the prior probability
					if numCauses == 0:
						priorProb = condProbList[0]

					# Creating dictionary and inserting in parsed data
					parsedData.append({
						'var':effectVariable,		# The variable
						'causeList':causeList,		# List of causes
						'PP':priorProb, 			# Prior Probability
						'numCauses':numCauses,		# Number of causes
						'condProbList':condProbList	# List of conditional probabilities
						})

				# Setting self.data to parsedData
				self.data = parsedData

				return self.data

		else: # Data has not yet been read / self.data is not a list

			if config.flag_show_errors:
				print
				print "### FATAL ERROR 3 [FileHelper.parseContents()]: self.data is not list"
				print

			return None


	def getAttributes(self, key): # Return the list of attributes

		attrList = None

		if self.data == None:

			if config.flag_show_errors:
				print
				print "### FATAL ERROR 3 [FileHelper.getAttributes()]: self.data is None"
				print

		else:

			if type(self.data[0]) == str:
				if config.flag_show_errors:
					print
					print "### FATAL ERROR 4 [FileHelper.getAttributes()]: self.data is not parsed"
					print

			else:

				if key not in self.data[0].keys():

					if config.flag_show_errors:
						print
						print "### FATAL ERROR 5 [FileHelper.getAttributes()]: invalid key."
						print "### List of keys =", self.data[0].keys()
						print "### Given key =", key
						print

				else:

					attrList = []

					for dat in self.data:
						attrList.append(dat[key])

		return attrList


	def preProcess(self, fileName): # Opens the file and preprocesses it (automate the 3 steps as given below)

		self.open(fileName)
		self.readFile()
		self.parseContents()
