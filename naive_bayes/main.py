import os
from parser import Parser
from classifier import Classifier

# data_path = "/home/lashit/AGM/GSoC/src/tests/"
data_path = "../tests/"
total_dirs = 5
train_dirs = 10

def enum(num_digits, count):
	numero = [0] * num_digits
	for i in range(num_digits):
		numero[i] = count % 10
		count = int(count/10)
	return ''.join(str(digit) for digit in reversed(numero))

p = Parser()
p.parse_domain(data_path + "domain.aggl")
c = Classifier(p.action_list)

for i in range(1, total_dirs + 1):
	path = data_path + enum(5, i) + "/"
	# One initModel.xml per dir
	p.parse_initM(path + enum(5, i) + ".xml")
	for file in os.listdir(path):
		if file.endswith(".aggt"):
			# try:
			# print(file)
			if os.stat(path + file + ".plan").st_size != 0:
				p.parse_target(path + file)
				p.parse_plan(path + file + ".plan")
				if i < train_dirs:
					c.train(p.attr_node + p.attr_link, p.tgt_actions)
				else:
					print(c.predict(p.attr_node + p.attr_link))
			# except:
			# 	pass
	print("At dir : ", i)
c.print_data()