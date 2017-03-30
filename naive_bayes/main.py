import os
from parser import Parser
from classifier import Classifier

data_path = "/home/lashit/AGM/GSoC/src/tests/"
total_dirs = 540

def enum(num_digits, count):
	numero = [0] * num_digits
	for i in range(num_digits):
		numero[i] = count % 10
		count = int(count/10)
	return ''.join(str(digit) for digit in reversed(numero))

p = parser()
p.parse_domain(data_path + "domain.aggl")
for i in range(1, total_dirs):
	path = data_path + enum(5, i)
	for file in os.listdir(path):
		p.parse_initM(path + "/" + enum(5, i) + ".xml")
		if file.endswith(".aggt"):
			print(file)
			# Figure out how to use file and all..
			# Append .plan to get all plan files