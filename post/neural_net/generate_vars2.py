import sys
sys.path.append("/usr/local/share/agm")
from parseAGGL import *

domainFile = "../../tests/domain.aggl"
agmData = AGMFileDataParsing.fromFile(domainFile)

types = list(agmData.agm.types.keys())
print 'types:', types


links = set([])
for rule in agmData.agm.rules:
	links |= set([ (rule.lhs.nodes[link.a].sType, link.linkType, rule.lhs.nodes[link.b].sType, link.enabled) for link in rule.lhs.links])
	links |= set([ (rule.rhs.nodes[link.a].sType, link.linkType, rule.rhs.nodes[link.b].sType, link.enabled) for link in rule.rhs.links])

links = list(links)
print 'links:', links



print '----'

inputVars = types + links
print '#i', len(inputVars)

outputVars = []
for rule in agmData.agm.rules:
	outputVars.append(rule.name)

print '#o', outputVars




