# import sys
# from test import *
#
# init_file   = '../../tests/00521/00521.xml'
# target_file = '../../tests/00521/054_targetMoveObjects.aggt'
# train_file  = 'store.data'
# threshold   = 0.1
# fileName    = 'xxxxxxxxxxxxx'
#
# t = Test()
# t.mono_test(init_file, target_file, train_file)
# t.new_domain(threshold, fileName)

import os, sys
import traceback
from parser import Parser
from classifier import Classifier
from test import Test, EmptyDomain

# data_path = "/home/lashit/AGM/GSoC/src/tests/"
data_path = "../../tests/"

# Enter all the directories to be trained here.
start_dir = 531
end_dir = 540
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

os.makedirs('benchmark')
for i in dirs:
	path = data_path + enum(5, i) + "/"
	domain = data_path + "domain.aggl"
	initial = path + enum(5, i) + ".xml"
	# One initModel.xml per dir
	flag = True
	try:
		p.parse_initM(path + enum(5, i) + ".xml")
	except:
		flag = False
		print("File not found : " + path + enum(5, i) + ".xml")
	if flag:
		print("At dir : ", i)
		newpath = 'benchmark/'+enum(5, i)
		if not os.path.exists(newpath):
			os.makedirs(newpath)
		for filename in os.listdir(path):
			if filename.endswith(".aggt"):
				if os.stat(path + filename + ".plan").st_size != 0:
					target = path + filename
					try:
						print domain, "--->",  initial, '--->', target
						newpath = 'benchmark/'+enum(5, i)+'/'+filename
						if not os.path.exists(newpath):
							os.makedirs(newpath)

						initialModel = data_path+enum(5, i)+"/"+enum(5, i)+".xml"
						targetFile = path + filename
						t = Test()
						try:
							t.mono_test(initialModel, targetFile, "store.data")
						except KeyError:
							continue
						print 'a'
						for th in [0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.7, 0.9]:
							print 'b', th
							domain = newpath+"/filtered_"+str(int(th*100)).zfill(10)+".aggl"
							try:
								t.new_domain(th, domain)
							except EmptyDomain:
								print 'empty domain'
								# os._exit(0)
								continue
							outfile = 'benchmark/'+enum(5, i)+'/'+filename
							estrin = "agglplan " + domain + ' ' + initialModel +  ' ' + targetFile + ' ' + outfile+str(int(th*100)).zfill(10)+'.plan'
							print '<'+estrin+'>'
							os.system(estrin)

					except:
						traceback.print_exc()
						pass
