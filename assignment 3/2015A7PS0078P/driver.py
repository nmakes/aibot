"""
	NAME: Naveen Venkat
	ID: 2015A7PS0078P
"""

from modules import *
import sys
import config

# DRIVER CODE

def displayMenu():
	print "1. Display the packages"
	print "2. Display the constraint graph (partially implemented)"
	print "3. Execute DFS + BT (incomplete)"
	print "4. Execute DFS + BT + Constraint Propagation (incomplete)"
	print "5. Exit"


def displayPackages(packages):
	print "-- Student Packages --"
	print

	print "packages for program A"
	for p in packages['student']['Program A']:
		print p
	print
	
	print "packages for program B"
	for p in packages['student']['Program B']:
		print p
	print
	
	print "packages for program C"
	for p in packages['student']['Program C']:
		print p
	print

	print "-- Professor Packages --"
	print

	for p in packages['professor']:
		print packages['professor'][p]
	print


def displayCG(cg):

	print "Nodes: "

	for n in cg.nodes:
		print n

	print 
	print "Edges: Not implemented fully"

TableData = [ 
				['c_01','prof-1','wednesday','10:00am','lecture','h_01'],
				['c_01','prof-1','monday','10:00am','lecture','h_01'],
				['c_01','prof-1','friday','1:00pm','lecture','l_02'],
				['c_02','prof-5','thursday','11:00am','lecture','h_05']
			]

if __name__=="__main__":

	config.testCaseFileName = raw_input("Enter Testcase file name: ")
	(packages, courseList, profList) = generate_packages(config.testCaseFileName)

	csp = CSP(courseList, profList)
	cg = CG(csp)

	while(True):
		displayMenu()
		inp = raw_input("Enter option: ")

		if int(inp)==1:
			displayPackages(packages)

		elif int(inp)==2:
			cg.constructCG(packages)
			displayCG(cg)

		elif int(inp)==5:
			break

		else:
			continue

# print dom
# print len(dom)
# print sys.getsizeof(dom)