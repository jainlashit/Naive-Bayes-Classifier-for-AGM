from __future__ import division
import json
import pickle

class Classifier:
	
	def __init__(self, action_list):
		self.laplace_constant = 1
		# Count number of training instances
		self.total_count = 0
		# Number of times action occured
		# Now we can calculate P(target) = self.action_count[target]/self.total_count
		self.action_count = {}
		'''Number of times attribute occurs given a target (action in .plan file)'''
		# This will help us calculate P(attribute | target)
		self.attr_count = {}
		# Contains list of all the attributes encountered.
		self.attr_all = []
		self.action_list = action_list
		for action in self.action_list:
			self.action_count[action] = 0
			self.attr_count[action] = {}

	def train(self, attr_list, tgt_actions):
		# attr_list contains both attr_node and attr_link [refer Parser class] (list of all the attributes)
		for action in tgt_actions:
			flag = True
			self.total_count += 1
			self.action_count[action] += 1
			for attr in attr_list:
				if attr not in self.attr_count[action]:
					self.attr_count[action][attr] = 1
					flag = False
					if attr not in self.attr_all:
						self.attr_all.append(attr)
				elif flag:
					flag = False
					self.attr_count[action][attr] += 1
				# else:
				# 	'''There is a chance that the following count can be greater than action_count[action]
				# 	 because we allow a single attribute to occur multiple times'''
				# 	self.attr_count[action][attr] += 1

	def print_data(self):
		f = open("total_count.txt", "w")
		f.write(str(self.total_count))
		f.close()
		json.dump(self.action_count, open("action_count.txt", "w"))
		f = open("attr_count.txt", "w")
		for key in self.attr_count:
			f.write(str(key) + ":" + str(self.attr_count[key]) + "\n")
		f.close()

	def prefetch(self, total_count, action_count, attr_count, attr_all, action_list):
		# In case data is already trained
		self.total_count = total_count
		self.action_count = action_count
		self.attr_count = attr_count
		self.attr_all = attr_all
		self.action_list = action_list


	def store(self):
		# stores data for further training purpose
		f = open("store.data", "wb")
		pickle.dump((self.total_count, self.action_count, self.attr_count, self.attr_all, self.action_list), f)
		f.close()
		
	def predict(self, attr_list):
		'''Provides a probability distribution over actions'''
		prob_action = {}
		for action in self.action_list:
			prob_action[action] = self.action_count[action] / self.total_count
			for attr in self.attr_all:
				prob_term = 1 / (self.action_count[action] + 2 * self.laplace_constant)
				if attr in self.attr_count[action]:
					prob_term *= (self.attr_count[action][attr] + self.laplace_constant)
					if attr in attr_list:
						prob_action[action] *= prob_term
					else:
						prob_action[action] *= 1 - prob_term
				else:
					prob_term *= self.laplace_constant
					if attr in attr_list:
						prob_action[action] *= prob_term
					else:
						prob_action[action] *= 1 - prob_term 
		return prob_action
