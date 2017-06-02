import sys
import pickle
from parser import Parser
from classifier import Classifier

def fetch(fileName):
	f = open(fileName, "rb")
	return pickle.load(f)



if __name__ == '__main__':
	p = Parser()
	c = Classifier([])
	# .plan file
	p.parse_plan(sys.argv[3])
	# .xml file
	p.parse_initM(sys.argv[1])
	# .aggt file
	p.parse_target(sys.argv[2])
	# Learning file
	temp = fetch(sys.argv[4])
	c.prefetch(*fetch(sys.argv[4]))
	print(c.predict(p.attr_link + p.attr_node))
