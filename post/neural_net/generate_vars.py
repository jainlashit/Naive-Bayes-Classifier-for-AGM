import sys
from sets import Set
sys.path.append("/usr/local/share/agm")
from parseAGGL import *

domainFile = "/home/lashit/AGM/GSoC/AGMWL/tests/domain.aggl"

agmData = AGMFileDataParsing.fromFile(domainFile)


types = Set([])
links = Set([])

# print("----nodeTypes----")
for rule in agmData.agm.rules:
	print rule
	types = types.union(set(rule.lhs.nodes.keys()))
	types = types.union(set(rule.rhs.nodes.keys()))
	# try:
	# 	types = types.union(rule.nodeTypes())
	# except:
	# 	# print rule
	# 	# print(rule.rhs.nodeTypes().union(rule.lhs.nodeTypes()))
	# 	pass
print(types)
# print("----nodeTypes----")

# print("----LinkTypes----")
for rule in agmData.agm.rules:
	try:
		links = links.union(rule.linkTypes())
	except:
		pass
print(links)
# print("----LinkTypes----")
