import graph
import re

def check_conflict_serializable(s):
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
			if read_write == 'r':
				temp = re.findall('w[^{0}]\({1}\)'.format(temp_num, attribute), original_s[x[1]:])
				if len(temp) != 0:
					for y in temp:
						temp_num = re.findall('[0-9]',y)
						result.append(int(temp_num[0]))
				else:
					continue
			elif read_write == 'R':
				temp = re.findall('W[^{0}]\({1}\)'.format(temp_num, attribute), original_s[x[1]:])
				if len(temp) != 0:
					for y in temp:
						temp_num = re.findall('[0-9]', y)
						result.append(int(temp_num[0]))
				else:
					continue
			elif read_write == 'w':
				temp = re.findall('r[^{0}]\({1}\)'.format(temp_num, attribute), original_s[x[1]:])
				if len(temp) != 0:
					for y in temp:
						temp_num = re.findall('[0-9]', y)
						result.append(int(temp_num[0]))
				else:
					continue
			elif read_write == 'W':
				temp = re.findall('R[^{0}]\({1}\)'.format(temp_num, attribute), original_s[x[1]:])
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
		