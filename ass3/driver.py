from modules import *
import sys
import config



# DRIVER CODE

(packages, courseList, profList) = generate_packages(config.testCaseFileName)

csp = CSP([], [])
domains = csp.initDomains()

# print dom
# print len(dom)
# print sys.getsizeof(dom)