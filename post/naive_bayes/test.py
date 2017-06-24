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
		prb_distrb = sorted(prb_distrb, key=prb_distrb.get, reverse=True)
		
		return prb_distrb

	def get_accuracy(self, plan_file):

		if os.stat(plan_file).st_size == 0:
			print("ERROR: Empty plan file")
			return

		accuracy = 0
		self.parser.parse_plan(plan_file)
		tgt_actions = self.parser.tgt_actions
		# print(tgt_actions)

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

	def new_domain(self, fraction, fileName, mode=True):
		'''
			mode = True => fraction will be taken as action count threshold
			mode = False => fraction will be taken as probability threshold
		'''
		if mode:
			toInclude = [action for action in self.prb_distrb[0:int(fraction*len(self.prb_distrb))]]
		else:
			toInclude = [action for action in self.prb_distrb if self.prb_distrb[action] >= fraction]

		if len(toInclude) == 0:
			print('empty domain', fileName)
			raise EmptyDomain('empty domain '+ fileName)
		f = open(fileName, 'w')
		# print(self.prb_distrb)
		f.write(AGMConst().visualParams)
		for action in toInclude:
			f.write(self.classifier.action_info[action])
		f.close()


	def batch_input(self, data_path, start_dir, end_dir):
		self.data_path = data_path
		# Enter all the directories to be trained here.
		self.dirs = range(start_dir, end_dir + 1)


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

	def batch_test(self, train_file):

		try:
			self.data_path
		except:
			print("ERROR: invoke batch_input(data_path, start_dir, end_dir) before batch testing")
			return

		self.classifier= Classifier([])
		self.parser= Parser()

		accuracy = 0
		min_accuracy = 100
		count = 0
		self.classifier.prefetch(*self.fetch(train_file))


		for i in self.dirs:
			flag = True
			path = self.data_path + self.enum(5, i) + "/"
			# One initModel.xml per dir
			try:
				self.parser.parse_initM(path + self.enum(5, i) + ".xml")
			except:
				flag = False
				print("File not found : " + path + self.enum(5, i) + ".xml")
				continue
		
			for file in os.listdir(path):
				if file.endswith(".aggt"):
					try:
						if os.stat(path + file + ".plan").st_size != 0:
							self.parser.parse_target(path + file)
							self.prb_distrb = self.normalize(self.classifier.predict(self.parser.attr_link + self.parser.attr_node))
							accuracy += self.get_accuracy(path + file + ".plan")
							count += 1
					except:
						pass

			print("At dir : ", i)
		try:
			accuracy /= count
			print("Accuracy : " + str(accuracy) + "%")
		except ZeroDivisionError:
			pass
			


if __name__ == '__main__':

	t = Test()
	'''
	Pass pickled data for batch testing. "python fileName learning_file"
	For singleton testing "python fileName initModel.xml target.aggt learning_file"
	'''

	if len(sys.argv) == 4:
		t.mono_test(sys.argv[1], sys.argv[2], sys.argv[3])
		for th in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]:
			t.new_domain(th, "filtered_"+str(int(th*100)).zfill(10)+".aggl")
	elif len(sys.argv) == 2:
		data_path = "../../tests/"
		start_dir = 542
		end_dir = 542
		t.batch_input(data_path, start_dir, end_dir)
		dirs = range(start_dir, end_dir + 1)
		t.batch_test(sys.argv[1])
	else:
		print("ERROR: Arguments missing")
		print("For Batch training syntax    : `$python test.py learning_file`")
		print("For Training single instance : `$python test.py initModel.xml target.aggt learning_file`")
