import os
from parser import Parser
from classifier import Classifier

# data_path = "/home/lashit/AGM/GSoC/src/tests/"
data_path = "../../tests/"

# Enter all the directories to be trained here.
start_dir = 1
end_dir = 270
dirs = range(start_dir, end_dir + 1)

def enum(num_digits, count):
	numero = [0] * num_digits
	for i in range(num_digits):
		numero[i] = count % 10
		count = int(count/10)
	return ''.join(str(digit) for digit in reversed(numero))

p = Parser()
p.parse_domain(data_path + "domain.aggl")
c = Classifier(p.action_list)

for i in dirs:
	path = data_path + enum(5, i) + "/"
	# One initModel.xml per dir
	try:
		p.parse_initM(path + enum(5, i) + ".xml")
		for file in os.listdir(path):
			if file.endswith(".aggt"):
				try:
					if os.stat(path + file + ".plan").st_size != 0:
						p.parse_target(path + file)
						p.parse_plan(path + file + ".plan")
						c.train(p.attr_node + p.attr_link, p.tgt_actions)
				except:
					pass
	except:
		print("File not found : " + path + enum(5, i) + ".xml")
	print("At dir : ", i)
c.store(p.action_info)
