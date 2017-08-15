import sys
sys.path.append("/usr/local/share/agm")
from parseAGGL import *

domainFile = "../../tests/domain.aggl"
agmData = AGMFileDataParsing.fromFile(domainFile)

types = agmData.agm.types.keys()
print 'types:', types


links = set([])
for rule in agmData.agm.rules:
	links |= set([link.linkType for link in rule.lhs.links+rule.rhs.links])
print 'types:', links
