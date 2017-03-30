#Generates plan for all the training dataset(without plan)
import os
data_path = "../test/"


def enum(num_digits, count):
	numero = [0] * num_digits
	for i in range(num_digits):
		numero[i] = count % 10
		count = int(count/10)
	return ''.join(str(digit) for digit in reversed(numero))

for i in range(1, 10):
	path = data_path + enum(5, i)
	for file in os.listdir(path):
		if file.endswith(".aggt"):
			command = "agglplan "
			command += data_path + "domain.aggl "
			command += path + "/" + enum(5, i) + ".xml "
			command += path + "/" + file + " "
			command += path + "/" + file.replace(".aggt", ".plan")
			os.system(command)

