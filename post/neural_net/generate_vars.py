import sys
from sets import Set
sys.path.append("/usr/local/share/agm")
from parseAGGL import *

domainFile = "../../tests/domain.aggl"

agmData = AGMFileDataParsing.fromFile(domainFile)


types = Set([])
links = Set([])

print("----nodeTypes (version 1)----")
for rule in agmData.agm.rules:
	try:
		types = types.union(rule.nodeTypes())
	except:
		# Except rule is for hierarchical actions
		pass
# Problem is that it doesn't output tableSt (because they are present in hierarchical rules)
print(types)
print("----nodeTypes (version 1)----")

print("----nodeTypes (version 2)----")
for rule in agmData.agm.rules:
	types = types.union(set(rule.lhs.nodes.keys()))
	types = types.union(set(rule.rhs.nodes.keys()))

# Problem is that it includes weird types like '12' 'rSt' which I think is not wanted
print(types)
print("----nodeTypes (version 2)----")




for rule in agmData.agm.rules:
	try:
		links = links.union(rule.linkTypes())
	except:
		pass
print(links)
# print("----LinkTypes----")
