# vmap = argmax P(a1, a2, .., an | vj) * P(vj)
# vmap = argmax P(a1 | vj) * P(a2 | vj) * .. * P(an | vj) * P(vj)

class Classifier:
	
	def __init__(self, attr_node, attr_link):
		self.attr_node = attr_node
		self.attr_link = attr_link

	def train(self):
		pass

	def predict(self):
		pass
