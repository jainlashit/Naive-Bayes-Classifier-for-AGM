from __future__ import division
import sys
import os
import pickle
from parser import Parser
from classifier import Classifier
import traceback
from const import AGMConst

class EmptyDomain (Exception):
	def __init__(self, text):
		self.text = text

class Test:

	def __init__(self):
		pass

	def fetch(self, fileName):
		f = open(fileName, "rb")
		return pickle.load(f)

	def normalize(self, prb_distrb):
		total = 0
		for action in prb_distrb:
			total += prb_distrb[action]
		for action in prb_distrb:
			prb_distrb[action] = prb_distrb[action]/total
		
		# Not necessary to sort but doing it for other methods like new_domain
		f = open("prb_distrb.prb", "w")
		pickle.dump(prb_distrb, f)
		f.close()
		prb_distrb = sorted(prb_distrb, key=prb_distrb.get, reverse=True)
		
		return prb_distrb


	def mono_test(self, init_file, target_file, train_file):
		'''
		For singleton testing pass pickled data from train.py . "python fileName initModel.xml target.aggt learning_file"
		'''
		self.classifier = Classifier([])
		self.parser = Parser()
		accuracy = 0
		min_accuracy = 100
		# .xml file
		self.parser.parse_initM(init_file)
		# .aggt file
		self.parser.parse_target(target_file)
		# train_file contains relevant trained data (pickled)
		self.classifier.prefetch(*self.fetch(train_file))
		self.prb_distrb = self.normalize(self.classifier.predict(self.parser.attr_link + self.parser.attr_node))



if __name__ == '__main__':

	t = Test()
	'''
	Pass pickled data for batch testing. "python fileName learning_file"
	For singleton testing "python fileName initModel.xml target.aggt learning_file"
	'''

	if len(sys.argv) == 4:
		t.mono_test(sys.argv[1], sys.argv[2], sys.argv[3])

	else:
		print("ERROR: Arguments missing")
		print("To generate valid prb file : `$python generate_prb.py initModel.xml target.aggt learning_file`")
