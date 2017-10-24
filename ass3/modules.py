import csv
import config
import itertools

def generate_packages(testCaseFileName):

	testCaseFile = open(testCaseFileName)
	linesRead = csv.reader(testCaseFile, delimiter=',')

	packages = { 
					"student":{ "Program A":[], "Program B":[], "Program C":[] },
					"professor":{}
				}

	courseList = {}
	professorList = {}
	
	programList = {}
	flag = 0 # not reading anything
	courseHeader = None
	profHeader = None

	courseInitFlag = 0

	for line in linesRead:
		
		if config.showFileRead: 
			print line

		if line[0] == '$COURSES$': # reinit flag
			flag = 0

		if line[0] == '$PROF$': # reinit flag
			flag = 0
		
		if line[0] == "Courses": # read the format of the csv file for course description
			flag = 1 # reading courses
			courseHeader = line
			programList[courseHeader[1]] = {}
			programList[courseHeader[2]] = {}
			programList[courseHeader[3]] = {}
		elif line[0] == 'Professor':
			flag = 2 # reading professors
		else:
			if flag==1:
				courseList[line[0]] = line
				if courseInitFlag==0:
					for i in range(3):
						programList[courseHeader[i+1]]['DC'] = []
						programList[courseHeader[i+1]]['DE'] = []
						programList[courseHeader[i+1]]['GE'] = []
						programList[courseHeader[i+1]]['NA'] = []
					courseInitFlag = 1

				programList[courseHeader[1]][line[1]].append(line[0])
				programList[courseHeader[2]][line[2]].append(line[0])
				programList[courseHeader[3]][line[3]].append(line[0])

			elif flag==2:
				professorList[line[0]] = line
				packages['professor'][line[0]] = []

				for i in range(1, 5):
					if line[i]=='NA':
						break
					else:
						packages['professor'][line[0]].append(line[i])

	# GENERATE STUDENT PACKAGES

	if config.verbose: print "\n------ generating packages ------\n"

	# student packages for program A
	subsetsA = []
	subsetsA.append(list(itertools.combinations(programList['Program A']['DC'], 3)))
	subsetsA.append(list(itertools.combinations(programList['Program A']['DE'], 2)))
	subsetsA.append(list(itertools.combinations(programList['Program A']['GE'], 1)))

	newList = []

	for sub0 in subsetsA[0]:
		for sub1 in subsetsA[1]:
			for sub2 in subsetsA[2]:
				newList.append( [ sub0, sub1, sub2 ] )

	if config.verbose:
		print "Student Packages for Program A:"
	for l in newList:
		if config.verbose:
			print l
		packages["student"]["Program A"].append(l)
	if config.verbose: print

	# student packages for program B
	subsetsB = []
	subsetsB.append(list(itertools.combinations(programList['Program B']['DC'], 3)))
	subsetsB.append(list(itertools.combinations(programList['Program B']['DE'], 2)))
	subsetsB.append(list(itertools.combinations(programList['Program B']['GE'], 1)))

	newList = []

	for sub0 in subsetsB[0]:
		for sub1 in subsetsB[1]:
			for sub2 in subsetsB[2]:
				newList.append( [ sub0, sub1, sub2 ] )
	
	if config.verbose: print "Student Packages for Program B:"
	for l in newList:
		if config.verbose: print l
		packages["student"]["Program B"].append(l)
	if config.verbose: print 

	# student packages for program C
	subsetsC = []
	subsetsC.append(list(itertools.combinations(programList['Program C']['DC'], 3)))
	subsetsC.append(list(itertools.combinations(programList['Program C']['DE'], 2)))
	subsetsC.append(list(itertools.combinations(programList['Program C']['GE'], 1)))

	newList = []

	for sub0 in subsetsC[0]:
		for sub1 in subsetsC[1]:
			for sub2 in subsetsC[2]:
				newList.append( [ sub0, sub1, sub2 ] )
	
	if config.verbose: print "Student Packages for Program C:"
	for l in newList:
		if config.verbose: print l
		packages["student"]["Program C"].append(l)
	if config.verbose: print

	# professor packages
	if config.verbose: 
		for key in packages['professor']:
			print "Professor Packages for", key
			print packages['professor'][key]
			print

	sortedCourseList = {}
	sortedProfList = {}

	for key in sorted(courseList.iterkeys()):
		sortedCourseList[key] = courseList[key]

	for key in sorted(professorList.iterkeys()):
		sortedProfList[key] = professorList[key]

	return (packages, sortedCourseList, sortedProfList)

class CSP:

	"""
		A typical assignment will be:
		(Course component, Day, Hour, Room)

		For eg.
		("L", "Mon", 3, "h2")
	"""

	def __init__(self, courseList, professorList):
		
		# Course List
		""" 
			courseList =
			[
				['C_01', 'DC', 'NA', 'DE', 3, 0, 3],
				['C_02', 'DC', 'NA', 'NA', 3, 0, 3],
				...
			]
		"""
		self.courseList = courseList

		# Professor List
		"""
			professorList =
			[
				['Prof-1', 'C_01', 'C_08', 'NA', 'NA'],
				['Prof-2', 'C_09', 'NA', 'NA', 'NA'],
				...
			]
		"""
		self.professorList = professorList


	def initDomains(self):
		days = ['mon', 'tue', 'wed', 'thu', 'fri']
		hours = [1,2,3,4,5,6,7]
		sathours = [1,2,3,4]
		rooms = ['h1','h2','h3','h4','h5','l1','l2','l3','l4','l5']

		dom = []

		for day in days:
			for hour in hours:
				for room in rooms:
					dom.append((day, hour, room))

		for hour in sathours:
			for room in rooms:
				dom.append(('sat', hour, room))

		return dom


	def isComplete(assignment):
		
		for keys in assignment:
			if assignment[keys] == None:
				return False

		return True

class CG:

	def __init__(self, csp):

		# nodes of CG
		self.nodes = []

		# domains of each node
		self.domains = {}	# { 'C_01':[] , ... }

		# edge list
		self.neighbours = {}

		# assignment will be made to each node
		self.assignment = {}	# { 'C_01': None , ...}

		for course in csp.courseList:
			self.nodes.append(course)
			self.neighbours[course] = [a for a in csp.courseList if a!=course]
			self.assignment[course] = None


	def backtrackingSearch(csp):

		if csp.isComplete(self.assignment):
			return self.assignment

		uVar = selectUnassignedVariable(csp)	# implement

		for value in OrderDomainValues(uVar, self.assignment, csp):	# implement
			inferences = None
			if isConsistent(value, self.assignment):	# implement
				self.assignment[uVar] = value
				inferences = inference(csp, uVar, value)
				if inferences!= None:
					for (i,j) in inferences:
						self.assignment[i] = j
					result = backtrackingSearch(self.assignment, csp)
					if result != None:
						return result
			# remove uVar and inferences from assignment
			self.assignment[uVar] = None
			for keys in inferences:
				self.assignment[keys] = None