'''
Parses domain.aggl, WorldModel.aggl, Target.aggt, results.plan file for Learning Data  
'''



import xml.etree.ElementTree as ET


class Parser:

	# Maps id to it's type

	def __init__(self):
		# action_list contains list of the actions
		self.action_list = []
		# Contains mapping of id to type
		self.typeMap = {}
		# Contains mapping of pair of id's to the relations the have
		self.relMap = {}
		# tgt_actions list of all target values (actions)
		self.tgt_actions = []
		# Below two variables starting with attr_ contains training attributes for our Naive Bayes Classifier
		self.attr_node = []
		# what relations would exist between pair of id's as per target's (planner's context) requirement
		self.attr_link = []
		# Tells about the parameters involved with different action (used for dynamically producing action files)
		self.action_info = {}

	def parse_domain(self, fileName):
		'''
		A parser for Domain Files (.aggl extension)
		This reads domain file and gathers knowledge about two variables:
		i) self.action_list contains is a list of names of action
		ii) self.action_info contains all description of an action (as in domain.aggl). 
			This is used if a reduced (limited actions) domain file needs to be generated.  
		'''
		f = open(fileName)
		parse_flag = False
		count = 0
		curr_action = None
		'''Since actions are out of all nested loops, 
		therefore count=0 indicates to get ready to read an action name. 
		'''
		for line in f:
			if "===" in line and not parse_flag:
				''' Ignore visual editor stuff, parsing starts after we encounter
				=== delimiter. 
				'''
				parse_flag = True
			elif parse_flag:
				# Assumption : { } and action name are not present on the same line
				if "{" in line:
					count += 1
				elif "}" in line:
					count -= 1
				elif count == 0 and line.strip() != "":
					if "hierarchical" in line:
						curr_action = line.split()[1]
						self.action_list.append(line.split()[1])
					else:
						curr_action = line.split()[0]
						self.action_list.append(line.split()[0])
					self.action_info[curr_action] = ''
				if curr_action != None:
					self.action_info[curr_action] += line
		
		f.close()

	def parse_initM(self, fileName):
		'''
		Parse initial world model (.xml extension)
		
		This functions fills-in following variables:
		i) typeMap : Maps id's to type
		ii) relMap : Contains relations between two id's
		'''
		
		# Re-initializing variables necessary while training and testing 
		self.typeMap = {}
		self.relMap = {}

		tree = ET.parse(fileName)
		root = tree.getroot()
		for child in root:
			if child.tag == "symbol":
				self.typeMap[int(child.attrib['id'])] = child.attrib['type']
			elif child.tag == "link":
				id1 = int(child.attrib['src'])
				id2 = int(child.attrib['dst'])
				id_pair = (id1, id2)
				if id_pair not in self.relMap:
					self.relMap[id_pair] = [child.attrib['label']]
				else:
					self.relMap[id_pair].append(child.attrib['label'])
	
	def parse_plan(self, fileName):
		'''
		Parses result file (.plan extension)
		Fills in self.tgt_actions which contains all the actions involved in the plan.
		'''
		self.tgt_actions = []
		f = open(fileName)
		for line in f:
			line = line.strip()
			if line.startswith("#!*"):
				line = line[3:].strip()
			elif line.startswith("*"):
				line = line[1:].strip()
			self.tgt_actions.append(line.split("@")[0])
		f.close()
	

	def parse_target(self, fileName):
		'''
		Parses target files (.aggt extension)
		'''
		self.attr_node = []
		self.attr_link = []
		# Keep tracks of keys used to represent some object type
		var_map = {}
		f = open(fileName)
		flag = False
		for line in f:
			if "{" in line:
				flag = True
			elif "}" in line:
				# Preconditions are not considered while learning.
				break
			if flag:
				if ":" in line:
					line = line.split(":")
					final_type = line[1].split("(")[0].strip()
					line[0] = line[0].strip() 
					# If id is given, initial type is matched to type of id
					if line[0].isdigit():
						init_type = self.typeMap[int(line[0])]
					else:
						''' If id is not given, initial type is assumed to be same as final type
						and the mapping is recorded.
						'''
						init_type = final_type
						var_map[line[0]] = final_type
					self.attr_node.append((init_type, final_type))

				elif "->" in line:
					line = line.split("->")
					temp = line[1].split("(")
					# line[0] basically represents src id
					line[0] = line[0].strip()
					# temp[0] basically represents dst id.
					temp[0] = temp[0].strip()
					# rel stores relations between two id's.
					rel = temp[1].split(")")[0].strip()


					# There can be four cases, src id is int/symbol or dst id is int/symbol
					if line[0].isdigit() and temp[0].isdigit():
						id1 = int(line[0])
						id2 = int(temp[0])
						id_pair = (id1, id2)
						type1 = self.typeMap[id1]
						type2 = self.typeMap[id2]

						self.attr_link.append((type1, rel, type2))
						if id_pair in self.relMap:
							for relation in self.relMap[id_pair]:
								self.attr_link.append((type1, relation, type2))
								self.attr_link.append((type1, relation, rel, type2))
							
					else:
						if not line[0].isdigit():
							if not temp[0].isdigit():
								type1 = var_map[line[0]]
								type2 = var_map[temp[0]]
								
								self.attr_link.append((type1, rel, type2))
								for id_pair in self.relMap:
									if type1 == self.typeMap[id_pair[0]] and type2 == self.typeMap[id_pair[1]]:
										for relation in self.relMap[id_pair]:
											self.attr_link.append((type1, relation, type2))
											self.attr_link.append((type1, relation, rel, type2))
											
							else:
								id2 = int(temp[0])
								type1 = var_map[line[0]]
								type2 = self.typeMap[id2]

								self.attr_link.append((type1, rel, type2))	
								for id_pair in self.relMap:
									if self.typeMap[id_pair[0]] == type1 and id_pair[1] == id2:
										for relation in self.relMap[id_pair]:
											self.attr_link.append((type1, relation, type2))
											self.attr_link.append((type1, relation, rel, type2))
										
						else:
							id1 = int(line[0])
							type1 = self.typeMap[id1]
							type2 = var_map[temp[0]]

							self.attr_link.append((type1, rel, type2))
							for id_pair in self.relMap:
								if id_pair[0] == id1 and self.typeMap[id_pair[1]] == type2:
									for relation in self.relMap[id_pair]:
										self.attr_link.append((type1, relation, type2))
										self.attr_link.append((type1, relation, rel, type2))

		f.close()


if __name__ == '__main__':
	p = Parser()
	main_path = "/home/lashit/AGM/GSoC/AGMWL/tests/"
	dir_num = "00001/"
	problem = "001_targetStop.aggt"
	p.parse_domain(main_path + "domain.aggl")
	p.parse_initM(main_path + dir_num + "00001.xml")
	p.parse_plan(main_path + dir_num + problem + ".plan")
	p.parse_target(main_path + dir_num + problem)
	print(p.tgt_actions)
	print(p.action_list)
