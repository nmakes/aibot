from modules import *
import sys
import config

# DRIVER CODE

def displayMenu():
	print "1. Display the packages"
	print "2. Display the constraint graph"
	print "3. Execute DFS+BT"
	print "4. Execute DFS + BT + Constraint Propagation"


TableData = [ 
				['c_01','prof-1','wednesday','10:00am','lecture','h_01'],
				['c_01','prof-1','monday','10:00am','lecture','h_01'],
				['c_01','prof-1','friday','1:00pm','lecture','l_02'],
				['c_02','prof-5','thursday','11:00am','lecture','h_05']
			]

def demoFunc():

	course = ['c_01', 'DC', 'NA', 'DE', '3 0 3']
	courseName = course[0]
	ltp = course[4]
	(lec,tut,prac) = ltp.split(' ')

	for l in range(int(lec)):
		varname = str(courseName)+' '+'L'+' '+str(l+1)
		print varname
		# self.nodes.append(varname)
		# self.domains.append[varname] = csp.initDomains()
		# createdVariables.append(varname)

	for t in range(int(tut)):
		varname = str(courseName)+' '+'T'+' '+str(t+1)
		print varname
		# self.nodes.append(varname)
		# self.domains.append[varname] = csp.initDomains()
		# createdVariables.append(varname)

	for p in range(int(prac)):
		
		varname = str(courseName)+' '+'P1'+' '+str(l+1)
		print varname
		# self.nodes.append(varname)
		# self.domains.append[varname] = csp.initDomains()
		# createdVariables.append(varname)

		varname = str(courseName)+' '+'P2'+' '+str(l+1)
		print varname
		# self.nodes.append(varname)
		# self.domains.append[varname] = csp.initDomains()
		# createdVariables.append(varname)

if __name__=="__main__":

	# config.testCaseFileName = raw_input("Enter Testcase file name: ")
	# (packages, courseList, profList) = generate_packages(config.testCaseFileName)

	# csp = CSP(courseList, profList)

	# displayTabularOutput(['Courses', 'Professor', 'Day', 'Time', 'L/T/P', 'Room'], TableData)

	demoFunc()

# print dom
# print len(dom)
# print sys.getsizeof(dom)