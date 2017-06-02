import sys
import pickle
from parser import Parser
from classifier import Classifier

def fetch(fileName):
	f = open(fileName, "rb")
	return pickle.load(f)

def get_accuracy(tgt_actions, prb_distrb):
	accuracy = 0
	for action in prb_distrb:
		if action in tgt_actions:
			accuracy += (prb_distrb[action]) * (prb_distrb[action])
		else:
			accuracy += (1 - prb_distrb[action]) * (1 - prb_distrb[action])
	accuracy /= len(prb_distrb)
	accuracy *= 100
	print(accuracy) 


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
	get_accuracy(p.tgt_actions, c.predict(p.attr_link + p.attr_node))
