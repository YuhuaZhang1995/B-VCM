### This part of the code process the input of the network data
### The input data takes the form of "node1\tnode2\tc1\tc2\n", with each line containing the node1, node2, block assignment of node1, and block assignment of node2

#count the number of senders

def preprocessing(filename,interactions,interactions3, interactions4,obs,count_all):
	# obs: list of list, [[s1,s2],...] 
	# count_all: dictionary, {node: count of the degree of nodes}
	# interactions: dictionary, {sender1: [receiver1 of node1,...]}
	# interactions4: dictionary, {sender1: {receiver1: # of interactions between of receiver 1 and node1,...}, node2:{},...}
	# interactions3: dictionary, {node: {node: # of iteractions between nodes,...},...}
	with open(filename) as infile:
		next(infile)
		for line in infile:
			s1=line.strip().split("\t")[0]
			s2=line.strip().split("\t")[1]
			#cs1=line.strip().split("\t")[2]
			#cs2=line.strip().split("\t")[3]

			obs.append([int(s1),int(s2)])
			if not int(s1) in count_all:
				count_all[int(s1)]=1
			else:
				count_all[int(s1)]+=1

			if not int(s2) in count_all:
				count_all[int(s2)]=1
			else:
				count_all[int(s2)]+=1

			if not int(s1) in interactions:
				interactions[int(s1)]=[int(s2)]
			else:
				interactions[int(s1)].append(int(s2))

			if not int(s1) in interactions3:
				interactions3[int(s1)]={int(s2):1}
			else:
				if not int(s2) in interactions3[int(s1)]:
					interactions3[int(s1)][int(s2)]=1
				else:
					interactions3[int(s1)][int(s2)]+=1
			if not int(s2) in interactions3:
				interactions3[int(s2)]={int(s1):1}
			else:
				if not int(s1) in interactions3[int(s2)]:
					interactions3[int(s2)][int(s1)]=1
				else:
					interactions3[int(s2)][int(s1)]+=1

			if not int(s1) in interactions4:
				interactions4[int(s1)]=[int(s2)]
			else:
				interactions4[int(s1)].append(int(s2))

			if not int(s2) in interactions4:
				interactions4[int(s2)]=[int(s1)]
			else:
				interactions4[int(s2)].append(int(s1))

	infile.close()


if __name__=="__main__":
	preprocessing(filename,interactions,interactions3, interactions4,obs,count_all)
