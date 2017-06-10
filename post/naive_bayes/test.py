from __future__ import division
import sys
import os
import pickle
from parser import Parser
from classifier import Classifier
import traceback

class Test:
	
	def __init__(self, data_path, start_dir, end_dir):
		self.data_path = data_path
		self.start_dir = start_dir
		self.end_dir = end_dir
		self.dirs = range(start_dir, end_dir + 1)

	def fetch(self, fileName):
		f = open(fileName, "rb")
		return pickle.load(f)

	def normalize(self, prb_distrb):
		total = 0
		for action in prb_distrb:
			total += prb_distrb[action]
		for action in prb_distrb:
			prb_distrb[action] = prb_distrb[action]/total
		return prb_distrb
		
	def get_accuracy(self, tgt_actions, prb_distrb):
		accuracy = 0
		# print(tgt_actions)
		self.prb_distrb = self.normalize(prb_distrb)
		for action in self.prb_distrb:
			if action in tgt_actions:
				accuracy += (self.prb_distrb[action]) * (self.prb_distrb[action])
			else:
				accuracy += (1 - self.prb_distrb[action]) * (1 - self.prb_distrb[action])
		accuracy /= len(self.prb_distrb)
		accuracy *= 100
		return accuracy


	def enum(self, num_digits, count):
		numero = [0] * num_digits
		for i in range(num_digits):
			numero[i] = count % 10
			count = int(count/10)
		return ''.join(str(digit) for digit in reversed(numero))

	def test(self):
		'''
		Pass pickled data for batch testing. "python fileName learning_file"
		For singleton testing "python fileName initModel.xml target.aggt final.plan learning_file"
		'''
		c = Classifier([])
		p = Parser()
		accuracy = 0
		min_accuracy = 100
		
		if len(sys.argv) == 5:
			# .plan file
			p.parse_plan(sys.argv[3])
			# .xml file
			p.parse_initM(sys.argv[1])
			# .aggt file
			p.parse_target(sys.argv[2])
			# Learning file
			c.prefetch(*self.fetch(sys.argv[4]))
			# print(c.attr_count)
			accuracy = self.get_accuracy(p.tgt_actions, c.predict(p.attr_link + p.attr_node))
			print("Accuracy : " + str(accuracy) + "%")

		elif len(sys.argv) == 2:
			count = 0
			c.prefetch(*self.fetch(sys.argv[1]))
			
			for i in self.dirs:
				flag = True
				path = self.data_path + self.enum(5, i) + "/"
				# One initModel.xml per dir
				try:
					p.parse_initM(path + self.enum(5, i) + ".xml")
				except:
					flag = False
					print("File not found : " + path + self.enum(5, i) + ".xml")

				if flag:		
					for file in os.listdir(path):
						if file.endswith(".aggt"):
							try:
								if os.stat(path + file + ".plan").st_size != 0:
									p.parse_target(path + file)
									p.parse_plan(path + file + ".plan")
							except:
								pass
						# print('Number of actions', len(p.tgt_actions))
						accuracy += self.get_accuracy(p.tgt_actions, c.predict(p.attr_link + p.attr_node))
						count += 1

					print("At dir : ", i)
			accuracy /= count
			print("Accuracy : " + str(accuracy) + "%")
		else:
			print("ERROR: Arguments missing")
			print("For Batch training syntax    : `$python test.py learning_file`")
			print("For Training single instance : `$python test.py initModel.xml target.aggt final.plan learning_file`")


if __name__ == '__main__':

	data_path = "../../tests/"
	# Enter all the directories to be trained here.
	start_dir = 271
	end_dir = 273

	t = Test(data_path, start_dir, end_dir)
	t.test()