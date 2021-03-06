import json
class Classifier:
	
	def __init__(self, action_list):
		self.laplace_constant = 1
		# Count number of training instances
		self.total_count = 0
		# Number of times action occured
		self.action_count = {}
		self.attr_count = {}
		self.action_list = action_list
		for action in self.action_list:
			self.action_count[action] = 0
			self.attr_count[action] = {}

	def train(self, attr_list, tgt_actions):
		# attr_list contains both attr_node and attr_link
		for action in tgt_actions:
			self.total_count += 1
			self.action_count[action] += 1
			for attr in attr_list:
				if attr not in self.attr_count[action]:
					self.attr_count[action][attr] = 1
				else:
					'''There is a chance that the following count can be greater than action_count[action]
					 because we allow a single attribute to occur multiple times'''
					self.attr_count[action][attr] += 1

	def print_data(self):
		f = open("total_count.txt", "w")
		f.write(str(self.total_count))
		f.close()
		json.dump(self.action_count, open("action_count.txt", "w"))
		f = open("attr_count.txt", "w")
		for key in self.attr_count:
			f.write(str(key) + ":" + str(self.attr_count[key]) + "\n")
		f.close()

	def predict(self, attr_list):
		# Provides a probability distribution over actions
		prob_action = {}
		for action in self.action_list:
			prob_action[action] = self.action_count[action] / self.total_count
			for attr in attr_list:
				if attr in self.attr_count[action]:
					prob_action[action] *= (self.attr_count[action][attr] + self.laplace_constant)
					# Number of values that an attribute can take is just one
					prob_action[action] /= (self.action_count[action] + self.laplace_constant)
				else:
					prob_action[action] *= (self.laplace_constant)
					prob_action[action] /= (self.action_count[action] + self.laplace_constant)
		return prob_action
