import os
import traceback
from parser import Parser
from classifier import Classifier


# data_path = "/home/lashit/AGM/GSoC/src/tests/"
data_path = "../../tests/"

# Enter all the directories to be trained here.
start_dir = 1
end_dir = 400
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
	flag = True
	try:
		p.parse_initM(path + enum(5, i) + ".xml")
	except:
		flag = False
		print("File not found : " + path + enum(5, i) + ".xml")
	if flag:
		for file in os.listdir(path):
			if file.endswith(".aggt"):
				if os.stat(path + file + ".plan").st_size != 0:
					try:
						p.parse_target(path + file)
						p.parse_plan(path + file + ".plan")
						c.train(p.attr_node + p.attr_link, p.tgt_actions)
					except:
						# traceback.print_exc()
						pass
	print("At dir : ", i)
c.store(p.action_info)
