"""
	NAME: Naveen Venkat
	ID: 2015A7PS0078P
"""

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
		(Day, Hour, Room)

		For eg.
		("Mon", 3, "h2")
	"""

	def __init__(self, courseList, professorList, domains=None):
		
		# Course List
		""" 
			courseList =
			{
				'C_01': ['C_01', 'DC', 'NA', 'DE', '3 0 3'],
				'C_02': ['C_02', 'DC', 'NA', 'NA', '3 0 3'],
				...
			}
		"""
		self.courseList = courseList

		# Professor List
		"""
			professorList =
			{
				'Prof-01': ['C_01', 'C_08', 'NA', 'NA'],
				'Prof-04': ['C_09', 'NA', 'NA', 'NA'],
				...
			}
		"""
		self.professorList = professorList

		# Domains
		
		if domains==None:
			self.domains = {}
			for key in courseList:
				self.domains[key] = self.initDomains()
		self.domains = domains


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

		# reference to csp object
		self.csp = csp

		# nodes of CG
		self.nodes = []

		# domains of each node
		self.domains = {}	# { 'C_01 L 1':[] , ... }

		# adjacency matrix
		self.neighbours = {}

		# assignment will be made to each node
		self.assignment = {}	# { 'C_01': None , ...}


	def createVariableNodes(self, courseName, program='prof'):

		course = self.csp.courseList[courseName]
		createdVariables = []

		if program == 'prof':
			ltp = course[4]
			(lec,tut,prac) = ltp.split(' ')

			# lectures
			for l in range(int(lec)):
				varname = str(courseName)+' '+'L'+' '+str(l+1)
				if config.verbose: print varname
				self.nodes.append(varname)
				self.domains[varname] = self.csp.initDomains()
				createdVariables.append(varname)

			# tutorials
			for t in range(int(tut)):
				varname = str(courseName)+' '+'T'+' '+str(t+1)
				if config.verbose: print varname
				self.nodes.append(varname)
				self.domains[varname] = self.csp.initDomains()
				createdVariables.append(varname)

			# practical section 1
			varname = str(courseName)+' '+'P1'
			if config.verbose: print varname
			self.nodes.append(varname)
			self.domains[varname] = self.csp.initDomains()
			createdVariables.append(varname)

			# practical section 2
			varname = str(courseName)+' '+'P2'
			if config.verbose: print varname
			self.nodes.append(varname)
			self.domains[varname] = self.csp.initDomains()
			createdVariables.append(varname)

		return createdVariables


	def constructCG(self, packages):

		studentPackages = packages['student']
		profPackages = packages['professor']

		for prof in profPackages:
			pack = profPackages[prof]
			for i in range(len(pack)-1):
				vars = self.createVariableNodes(pack[i])


		""" 
			PREPROCESSING STEP
			ADDING CONSTRAINT INFORMATION TO EDGES, AND RESTRICTING THE DOMAINS
		"""

		for var in self.nodes: # for every variable, restrict the domain (apply unary constraints)

			clist = var.split()
			courseName = clist[0]
			component = clist[1]
			rank = clist[2]

			"""
				Laboratory_Constraint_1: Laboratory sessions cannot be held in the forenoon
			"""
			if component in ['P1', 'P2']:
				dom = self.domains[var]
				self.domains[var] = [v for v in dom if v[1]>4]

			"""
				Professor_Constraint_8: Professor Prof-04 does not want to teach on Thursday while
				   						Professor Prof-01 can only teach during 9:00 AM to 11:00 AM.
			"""
			if (courseName in self.csp.professorList['Prof-4']) & (component=='L'):
				dom = self.domains[var]
				self.domains[var] = [v for v in dom if v[0]!='thu']

			if (courseName in self.csp.professorList['Prof-1']) & (component=='L'):
				dom = self.domains[var]
				self.domains[var] = [v for v in dom if v[1]<=2]

		#2. Laboratory sessions are consecutive for the given number of hours.
		""" @TODO """

		"""
			EDGE INTRODUCTION STEP
			HERE WE TAKE THE PACKAGES, AND INTRODUCE EDGES BETWEEN THE VARIABLES OF THE CG
			ACCORDINGLY, WE MARK THE VARIOUS CONSTRAINTS IN THE EDGES
		"""

		
		

def tutorial_constraint_3(csp, cg, from_node, to_node):
	"""
		Tutorial class can be conducted in forenoon or afternoon anytime, but 
		cannot be held on the same day of the lecture of the corresponding course.
	"""

	c1 = cg.assignment[from_node]
	c2 = cg.assignment[to_node]

	return (c1[0] != c2[0]) # if days are different, True is returned, otherwise return false


def disciplinary_constraint_4(csp, cg, from_node, to_node):
	"""
		No two disciplinary core courses of a program can be in succession.
	"""

	c1 = cg.assignment[from_node]
	c2 = cg.assignment[to_node]

	if c1[0] != c2[0]: # if days are different, True
		return True
	else: # otherwise
		if (c1[1] == c2[1] + 1) or (c1[1] == c2[1] - 1): # if hour for both courses is consecutive then return False
			return False
		else: # otherwise True
			return True


def general_constraint_5(csp, cg, from_node, to_node):
	"""
		The general elective courses cannot be scheduled on the same day.
	"""

	c1 = cg.assignment[from_node]
	c2 = cg.assignment[to_node]

	return (c1[0] != c2[0]) # if days are different, True is returned, otherwise return false


def lecture_constraint_6(csp, cg, from_node, to_node):
	"""
		At the most one lecture for a course can be scheduled on a day.
	"""

	c1 = cg.assignment[from_node]
	c2 = cg.assignment[to_node]

	return (c1[0] != c2[0]) # if days are different, True is returned, otherwise return false


def laboratory_constraint_7(csp, cg, from_node, to_node):
	"""
		The student strength in each program is divided in two batches for
		their lab sessions. Therefore, a laboratory session is required to be
		scheduled twice a week for two batches of a course.
	"""

	c1 = cg.assignment[from_node]
	c2 = cg.assignment[to_node]

	return (c1[0] != c2[0]) # if days are different (twice a week), True is returned, otherwise return false


def professor_constraint_9(csp, cg, from_node, to_node):
	"""
		No professor should have two or more lectures/ lab sessions in succession. 
		This means that lectures or lab sessions to be taught by a professor should 
		have at least an hour gap.
	"""

	c1 = cg.assignment[from_node]
	c2 = cg.assignment[to_node]

	if c1[0] != c2[0]: # if days are different, return True
		return True
	else: # otherwise
		if (c1[1] == c2[1] + 1) or (c1[1] == c2[1] - 1): # if hour for both courses is consecutive then return False
			return False
		else: # otherwise return True
			return True


def student_constraint_10(csp, cg, from_node, to_node):
	"""
		No student should suffer a clash of time slots for chosen course package.
	"""

	c1 = cg.assignment[from_node]
	c2 = cg.assignment[to_node]

	return not((c1[0]==c2[0]) and (c1[1]==c2[1])) # if the two courses are not at the same day and time, then return True


def professor_constraint_11(csp, cg, from_node, to_node):
	"""
		No professor should suffer a clash of time slots for the courses to be
		taught by her or him.
	"""

	c1 = cg.assignment[from_node]
	c2 = cg.assignment[to_node]

	return not((c1[0]==c2[0]) and (c1[1]==c2[1])) # if the two courses are not at the same day and time, then return True