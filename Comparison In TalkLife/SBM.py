import pysbm
import networkx as nx
import pandas as pd
import numpy as np
import collections
import sys
from scipy import linalg
import random

K=int(sys.argv[2])

filename=sys.argv[1]
infile=open(filename)
next(infile)
int_dic={}
for line in infile:
	s1=int(line.strip().split("\t")[0])
	s2=int(line.strip().split("\t")[1])
	cs1=int(line.strip().split("\t")[2])
	cs2=int(line.strip().split("\t")[3])
	Q=int(line.strip().split("\t")[4])

	if not 'node1' in int_dic:
		int_dic['node1']=[s1]
	else:
		int_dic['node1'].append(s1)
	if not 'node2' in int_dic:
		int_dic['node2']=[s2]
	else:
		int_dic['node2'].append(s2)

infile.close()

rela=pd.DataFrame(int_dic)
G = nx.from_pandas_edgelist(rela, 'node1', 'node2', create_using=nx.Graph())
standard_partition = pysbm.NxPartition(graph=G,number_of_blocks=K)
standard_objective_function = pysbm.TraditionalUnnormalizedLogLikelyhood(is_directed=False)
standard_inference = pysbm.MetropolisHastingInference(G, standard_objective_function, standard_partition)
standard_inference.infer_stochastic_block_model()
output=[standard_partition.get_block_of_node(node) for node in G]
nodelist=[node for node in G]
for i in range(len(output)):
	print([nodelist[i],output[i]])
#print(output)
#print(nodelist)
