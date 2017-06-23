import xml.etree.ElementTree as ET


class Parser:

	# Maps id to it's type

	def __init__(self):
		# Maps id's to it's type
		self.typeMap = {}
		# Maps id pair to list of all relations they have
		self.relMap = {}
		# action_list contains list of all possible actions
		self.action_list = []
		# tgt_actions list of all actions used for achieving target
		self.tgt_actions = []
		self.attr_node = []
		self.attr_link = []

	def parse_domain(self, fileName):
		'''
		A parser function for files with .aggl extension
		'''
		f = open(fileName)
		parse_flag = False
		count = 0
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
						self.action_list.append(line.split()[1])
					else:
						self.action_list.append(line.split()[0])
		f.close()
	
	def parse_plan(self, fileName):
		'''
		A parser function for files with .plan extension
		'''
		f = open(fileName)
		for line in f:
			line = line.strip()
			if line.startswith("#!*"):
				line = line[3:].strip()
			elif line.startswith("*"):
				line = line[1:].strip()
			self.tgt_actions.append(line.split("@")[0])
		f.close()
	
	def parse_initM(self, fileName):
		'''
		Parse xml file (initial world model)
		'''
		tree = ET.parse(fileName)
		root = tree.getroot()
		for child in root:
			if child.tag == "symbol":
				self.typeMap[int(child.attrib['id'])] = child.attrib['type']
			elif child.tag == "link":
				id1 = int(child.attrib['src'])
				id2 = int(child.attrib['dst'])
				if id_pair not in self.relMap:
					self.relMap[id_pair] = [child.attrib['label']]
				else:
					self.relMap[id_pair].append(child.attrib['label'])

	def parse_target(self, fileName):
		'''
		Parse files with .aggt extension (target files)
		'''
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
					# If id is given, inital type is matched to type of id
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


						for relation in self.relMap[id_pair]:
							self.attr_link.append((relation, type1, type2, rel))
							
					else:
						if not line[0].isdigit():
							if not temp[0].isdigit():
								for id_pair in self.relMap:
									flag = False
									type1 = self.typeMap[id_pair[0]]
									type2 = self.typeMap[id_pair[1]]
									if line[0] == type1 and temp[0] == type2:
										flag = True
									for relation in self.relMap[id_pair]:
										self.attr_link.append((relation, type1, type2, rel))


							else:
								id2 = int(temp[0])
								for id_pair in self.relMap:
									flag = False
									if id2 in id_pair:
										if id2 == id_pair[0]:
											if self.typeMap[id_pair[1]] == var_map[line[0]]:
												flag = True
										else:
											if self.typeMap[id_pair[0]] == var_map[line[0]]:
												flag = True
									if flag:
										for relation in self.relMap[id_pair]:
											self.attr_link.append((relation, var_map[line[0]], self.typeMap[id2], rel))
						else:
							id1 = int(line[0])
							for id_pair in self.relMap:
								flag = False
								if id1 in id_pair:
									if id1 == id_pair[0]:
										if self.typeMap[id_pair[1]] == var_map[temp[0]]:
											flag = True
									else:
										if self.typeMap[id_pair[0]] == var_map[temp[0]]:
											flag = True
								if flag:
									for relation in self.relMap[id_pair]:
										self.attr_link.append((relation, self.typeMap[id1], var_map[temp[0]], rel))

		# print(var_map)
		f.close()

# if __name__ == '__main__':
# 	p = Parser()
# 	p.parse_domain("/home/lashit/AGM/GSoC/src/tests/domain.aggl")
# 	p.parse_plan("/home/lashit/AGM/GSoC/src/tests/00001/001_targetStop.aggt.plan")
# 	p.parse_initM("/home/lashit/AGM/GSoC/src/tests/00001/00001.xml")
# 	p.parse_target("/home/lashit/AGM/GSoC/src/tests/00001/001_targetStop.aggt")
# 	print(p.tgt_actions)
# 	print(p.action_list)
