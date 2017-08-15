import sys
sys.path.append("/usr/local/share/agm")
from parseAGGL import *

domainFile = "../../tests/domain.aggl"
agmData = AGMFileDataParsing.fromFile(domainFile)

types = list(agmData.agm.types.keys())
# print 'types:', types


links = set([])
for rule in agmData.agm.rules:
	links |= set([link.linkType for link in rule.lhs.links+rule.rhs.links])

links = list(links)

# print 'links:', links

inputVars = []
outputVars = []

for type1 in types:
	for type2 in types:
		inputVars.append((type1, type2))
		for link1 in links:
			inputVars.append((type1, link1, type2))
			for link2 in links:
				inputVars.append((type1, link1, link2, type2))

print len(inputVars)

agmData = AGMFileDataParsing.fromFile(domainFile)
for rule in agmData.agm.rules:
	outputVars.append(rule.name)

print outputVars




