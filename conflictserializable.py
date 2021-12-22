import graph
import re
from collections import defaultdict
from io import BytesIO
import matplotlib.pyplot as plt
import base64
import networkx as nx

def check_conflict_serializable(s):
	
	def check_format(str):
		str.strip()
		revised_str = ''
		for x in str:
			if x != ' ' and x != ',':
				revised_str += x

		schedule_len = [len(x) for x in re.findall('[rwRW][0-9]\([a-zA-Z]\)', revised_str)]

		return sum(schedule_len) == len(revised_str)
	
	if not check_format(s):
		return 'The input schedule is invalid, please try again'
	
	
	nums = set(re.findall('[0-9]', s))
	temp = []
	for x in nums:
		temp.append(int(x))

	nums = sorted(temp)

	def find_num_behind(temp_list, original_s):
		result = []
		for x in temp_list:
			single_schedule = original_s[x[0]:x[1]]
			temp_num = single_schedule[1]
			read_write = single_schedule[0]
			attribute = single_schedule[-2]
			if read_write == 'r' or read_write == 'R':
				temp = re.findall('[Ww][^{0}]\({1}\)'.format(temp_num, attribute), original_s[x[1]:])
				if len(temp) != 0:
					for y in temp:
						temp_num = re.findall('[0-9]',y)
						result.append(int(temp_num[0]))
				else:
					continue
			elif read_write == 'w' or read_write == 'W':
				temp = re.findall('[rR][^{0}]\({1}\)'.format(temp_num, attribute), original_s[x[1]:])
				if len(temp) != 0:
					for y in temp:
						temp_num = re.findall('[0-9]', y)
						result.append(int(temp_num[0]))
				else:
					continue
		return result

	temp_behind_result = []
	for x in nums:
		#if break_counter == 1:
		#    break
		temp_list = [m.span() for m in re.finditer('[a-zA-Z]{}\s*\([a-zA-Z]\)'.format(x), s)]
		num_behind = find_num_behind(temp_list, s)
		num_behind = [x] + num_behind
		temp_behind_result.append(num_behind)

	g = graph.Graph(len(nums))

	for x in temp_behind_result:
		if len(x) >= 2:
			for y in x[1:]:
				g.addEdge(x[0], y)
				
		
	if g.isCyclic():
		return 'This is cyclic and thus NOT conflict-serializable'
	else:
		return 'This is acyclic and thus conflict-serializable'

		
def draw_graph(str):

	nums = set(re.findall('[0-9]', str))
	temp = []
	for x in nums:
		temp.append(int(x))

	nums = sorted(temp)

	def find_num_behind(temp_list, original_s):
		result = []
		for x in temp_list:
			single_schedule = original_s[x[0]:x[1]]
			temp_num = single_schedule[1]
			read_write = single_schedule[0]
			attribute = single_schedule[-2]
			if read_write == 'r' or read_write == 'R':
				temp = re.findall('[Ww][^{0}]\({1}\)'.format(temp_num, attribute), original_s[x[1]:])
				if len(temp) != 0:
					for y in temp:
						temp_num = re.findall('[0-9]',y)
						result.append(int(temp_num[0]))
				else:
					continue
			elif read_write == 'w' or read_write == 'W':
				temp = re.findall('[rR][^{0}]\({1}\)'.format(temp_num, attribute), original_s[x[1]:])
				if len(temp) != 0:
					for y in temp:
						temp_num = re.findall('[0-9]', y)
						result.append(int(temp_num[0]))
				else:
					continue
		return result

	temp_behind_result = []
	for x in nums:
		#if break_counter == 1:
		#    break
		temp_list = [m.span() for m in re.finditer('[a-zA-Z]{}\s*\([a-zA-Z]\)'.format(x), str)]
		num_behind = find_num_behind(temp_list, str)
		num_behind = [x] + num_behind
		temp_behind_result.append(num_behind)

	edges = []

	for x in temp_behind_result:
		if len(x) >= 2:
			for y in x[1:]:
				edges.append((x[0], y))
	
	G = nx.MultiDiGraph()
	
	G.add_edges_from(edges)

	fig = plt.figure(figsize=(4,4))
	nx.draw(G, connectionstyle='arc3, rad = 0.3',
			with_labels=True, edgecolors='black',
			node_color='yellow', node_size=1000, width=3)
	
	return fig
		