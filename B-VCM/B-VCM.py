import numpy as np
import math
import scipy.optimize as opt
from scipy.optimize import minimize
import sys
import datetime
from pre_processing import preprocessing
from e2_llk import llk
from degree_count import degree_count

t1=datetime.datetime.now()


## Input commands propressing

command=sys.argv[1:]
Flag_pl=False
Flag_css=False
Flag_llk=False
Flag_B=False
K=2 #If no input, assume the underlying community is 2
iters=2000 #iteration=2000 by default
burn_in=1000 #burnt-in=1000 by default

for i in range(len(command)):
	if command[i]=="--iter":
		iters=int(command[i+1])
	if command[i]=="--burn-in":
		burn_in=int(command[i+1])
	if command[i]=="--input-file":
		filename=command[i+1]
	if command[i]=="--output-powerlaw":
		Flag_pl=True
	if command[i]=="--output-cluster":
		Flag_css=True
	if command[i]=="--output-llk":
		Flag_llk=True
	if command[i]=="--output-propensity":
		Flag_B=True
	if command[i]=="--K":
		K=int(command[i+1])

## Network data preprocessing

obs=[] # list of list, [[s1,s2],...] 
count_all={} # dictionary, {node: count of the degree of nodes}
interactions={} #  dictionary, {sender1: [receiver1 of node1,...]}
interactions3={} # dictionary, {sender1: {receiver1: # of interactions between of receiver 1 and node1,...}, node2:{},...}
interactions4={} # dictionary, {node: {node: # of iteractions between nodes,...},...}

preprocessing(filename,interactions,interactions3, interactions4,obs,count_all)


## Initialization model parameters

# Number of clusters and hyperparameters
alpha_zero=[1]*K # Prior for \pi 
a=[1]*K # Prior for theta
b=[1]*K # Prior for theta
c=[1]*K # Prior for alpha
d=[1]*K # Prior for alpha
Bb=np.ones((K,K)) # Prior for Propensity matrix

# Initialize B, alpha_C, theta_C
B=np.ones((K,K))/K # Propensity matrix
alpha_C=np.ones(K)/2 
theta_C=np.ones(K)*10

# Initialize block assignment C_s
N=len(count_all) #Number of nodes in the network
s_list=list(count_all.keys()) # nodelist
s_list.sort()
cluster_ass={} # block assignment for each node
for i in range(0,N):
	cluster_ass[s_list[i]]=np.where(np.random.multinomial(1,[0.5,0.5])==1)[0][0]


## Statistics of the network data

"""We have 3 parameters in updating the e2 llk: total deg(a scalar for each block), num_vertex(a scalar for each block), count_tmp(a dict), count_KK(scalar)"""
# (1) total_deg={1:tot_deg,2:tot_deg,...,K:tot_deg}
# (2) num_vertex={1:num_vex, 2:num_vex,...,K:num_vex}
# (3) count={1:{deg1:#,deg2:#,...,degN:#},2:{deg1:#,deg2:#,...,degN:#},...,K:{deg1:#,deg2:#,...,degN:#}}
# (4) count_KK={1:init#, 2:init#,...,K:init#}

total_deg_K={}
num_vertex_K={}
count_K={}
count_KK={}

degree_count(total_deg_K, num_vertex_K, count_K, count_KK, cluster_ass, interactions, count_all, K)


## Gibbs sampling

# Define Outcomes
clus_out={} # Cluster assignment in Gibbs sampler, dict: {1:[# of hits in Gibbs of node1, # of hits in Gibbs of node2,...], 2:[],...,k:[]}
for k in range(0,K):
	clus_out[k]=np.zeros(len(s_list))
LRT=[] # Marginal likelihood over the Gibbs samples
power_law=[] # power-law parameters, list: [[[alpha],[theta]] in iter 1,...]
propensity_matrix=[] #Propensity matrix, list: [[propensity matrix in iter 1],...]

# Gibbs Iterations
for iter in range(0,iters):
		
	#Update C_s
	for s in range(0,N):
		tmp_p=np.zeros(K)
		for k in range(0,K):
			### if the node is in cluster k:
			### just calculate the llk is enough 
			if cluster_ass[s_list[s]]==k:
				for kk in range(0,K):
					p=-llk(num_vertex_K[kk],total_deg_K[kk],count_K[kk],[alpha_C[kk],theta_C[kk]])
					tmp_p[k]=tmp_p[k]+p
					p=math.lgamma(alpha_zero[kk]+count_KK[kk])-math.lgamma(alpha_zero[kk])
					tmp_p[k]=tmp_p[k]+p
				p=0
				nn=0
				tmp_list=np.array(interactions4[s_list[s]])
				nn=len(tmp_list)
				p=p+math.lgamma(nn+1)
				ct=np.zeros(K)
				for sct in tmp_list:
					for kk in range(0,K):
						if cluster_ass[sct]==kk:
							ct[kk]+=1
							p=p+math.log(B[k,cluster_ass[sct]])
				for kk in range(0,K):
					p=p-math.lgamma(ct[kk]+1)
				tmp_p[k]=tmp_p[k]+p
				
			### if the node is not in cluster k:
			### need to remove the node from the original cluster assignment and add it to cluster k
			else:
				for kk in range(0,K):
					#add to cluster k
					if kk==k:
						if count_all[s_list[s]] in count_K[kk]:
							count_K[kk][count_all[s_list[s]]]=count_K[kk][count_all[s_list[s]]]+1
						else:
							count_K[kk][count_all[s_list[s]]]=1
						p=-llk(num_vertex_K[kk]+1,total_deg_K[kk]+count_all[s_list[s]],count_K[kk],[alpha_C[kk],theta_C[kk]])
						count_K[kk][count_all[s_list[s]]]=count_K[kk][count_all[s_list[s]]]-1
						tmp_p[k]=tmp_p[k]+p
						if s_list[s] in interactions:
							p=math.lgamma(alpha_zero[kk]+count_KK[kk]+len(interactions[s_list[s]]))-math.lgamma(alpha_zero[kk])
						else:
							p=math.lgamma(alpha_zero[kk]+count_KK[kk])-math.lgamma(alpha_zero[kk])
						tmp_p[k]=tmp_p[k]+p
					
					#remove the node from the original cluster assignment
					elif kk==cluster_ass[s_list[s]]:
						count_K[kk][count_all[s_list[s]]]=count_K[kk][count_all[s_list[s]]]-1
						p=-llk(num_vertex_K[kk]-1,total_deg_K[kk]-count_all[s_list[s]],count_K[kk],[alpha_C[kk],theta_C[kk]])
						if count_all[s_list[s]] in count_K[kk]:
							count_K[kk][count_all[s_list[s]]]=count_K[kk][count_all[s_list[s]]]+1
						else:
							count_K[kk][count_all[s_list[s]]]=1
						tmp_p[k]=tmp_p[k]+p
						if s_list[s] in interactions:
							p=math.lgamma(alpha_zero[kk]+count_KK[kk]-len(interactions[s_list[s]]))-math.lgamma(alpha_zero[kk])
						else:
							p=math.lgamma(alpha_zero[kk]+count_KK[kk])-math.lgamma(alpha_zero[kk])
						tmp_p[k]=tmp_p[k]+p
					
					else:
						p=-llk(num_vertex_K[kk],total_deg_K[kk],count_K[kk],[alpha_C[kk],theta_C[kk]])
						tmp_p[k]=tmp_p[k]+p
						p=math.lgamma(alpha_zero[kk]+count_KK[kk])-math.lgamma(alpha_zero[kk])
						tmp_p[k]=tmp_p[k]+p
				
				#Propensidy matrix
				p=0
				nn=0
				tmp_list=np.array(interactions4[s_list[s]])
				nn=len(tmp_list)
				p=p+math.lgamma(nn+1)
				ct=np.zeros(K)
				for sct in tmp_list:
					for kk in range(0,K):
						if cluster_ass[sct]==kk:
							ct[kk]+=1
							p=p+math.log(B[k,cluster_ass[sct]])
				for kk in range(0,K):
					p=p-math.lgamma(ct[kk]+1)
				tmp_p[k]=tmp_p[k]+p

		###sample cluster assignment
		if (np.unique(tmp_p)[-1]-np.unique(tmp_p)[-2])>30:
			# in case the probability differs too much, and 0 is generated
			new_ass=np.where(tmp_p==max(tmp_p))[0][0]
		else:
			tmp_p=np.array(tmp_p)-max(tmp_p)
			for kk in range(0,K):
				tmp_p[kk]=math.exp(tmp_p[kk])
			tmp_p=np.array(tmp_p)/sum(np.array(tmp_p))
			new_ass=np.where(np.random.multinomial(1,tmp_p)==1)[0][0]
		
		###If the newly sampled cluster is different from the cluster in the previous iteraction
		if cluster_ass[s_list[s]]!=new_ass:
			#remove from the old
			total_deg_K[cluster_ass[s_list[s]]]-=count_all[s_list[s]]
			num_vertex_K[cluster_ass[s_list[s]]]-=1
			count_K[cluster_ass[s_list[s]]][count_all[s_list[s]]]-=1
			if s_list[s] in interactions:
				count_KK[cluster_ass[s_list[s]]]-=len(interactions[s_list[s]])
			
			#add toward the new
			total_deg_K[new_ass]+=count_all[s_list[s]]
			num_vertex_K[new_ass]+=1
			if count_all[s_list[s]] in count_K[new_ass]:
				count_K[new_ass][count_all[s_list[s]]]=count_K[new_ass][count_all[s_list[s]]]+1
			else:
				count_K[new_ass][count_all[s_list[s]]]=1
			if s_list[s] in interactions:
				count_KK[new_ass]+=len(interactions[s_list[s]])

			cluster_ass[s_list[s]]=new_ass

	#update alpha_c and theta_c
	for k in range(0,K):
		#num_vertex=len(np.where(C_s==k)[0])
		#s_tmp=np.array(s_list)[np.where(C_s==k)[0]]
		s_tmp=np.array([key for key, value in cluster_ass.items() if value == k])
		num_vertex=len(s_tmp)
		count_tmp= {tt: count_all[tt] for tt in s_tmp if tt in count_all}
		count={}
		for i in count_tmp.keys():
			if count_tmp[i] in count.keys():
				count[count_tmp[i]]+=1
			else:
				count[count_tmp[i]]=1

		total_deg=list(count_tmp.values())
		total_deg=sum(total_deg)

		x=np.random.beta(theta_C[k]+1,total_deg-1)
		y=0
		for i in range(0,num_vertex-1):
			y=y+np.random.binomial(1,(theta_C[k]/(theta_C[k]+alpha_C[k]*(i+1))))
		z=0
		for i in count_tmp:
			for j in range(0,count_tmp[i]-1):
				z=z+1-np.random.binomial(1,(j/(j+1-alpha_C[k])))
		alpha_C[k]=np.random.beta(c[k]+num_vertex-1-y,d[k]+z)
		theta_C[k]=np.random.gamma(y+a[k],1/(b[k]-np.log(x)))
	
	#update B
	for i in range(0,K):
		tmp_alpha=[]
		for j in range(0,K):
			#B[i,j]=len(obs[where(s1 in i),where(s2 in j)])/len(obs[where s1 in j])
			count1=0
			count2=0
			for mm in obs:
				#s1=np.where(np.array(s_list)==mm[0])[0]
				#s2=np.where(np.array(s_list)==mm[1])[0]
				#if count_all[mm[0]]!=1 and count_all[mm[1]]!=1:
				if cluster_ass[mm[0]]==i:
					count1+=1
					if cluster_ass[mm[1]]==j:
						count2+=1
			tmp_alpha.append(count2)
		B[i,:]=np.random.dirichlet(tmp_alpha+np.array(Bb[i,:])[0],1)[0]				

	tmp_LRT=0
	for kk in range(0,K):
		tmp_LRT=tmp_LRT-llk(num_vertex_K[kk],total_deg_K[kk],count_K[kk],[alpha_C[kk],theta_C[kk]])
		s_tmp=np.array([key for key, value in cluster_ass.items() if value == kk])
		for kkk in range(0,K):
			s_tmp2=np.array([key for key, value in cluster_ass.items() if value == kkk])
			count_kk_kkk=0 #count of connect between kk and kkk
			for s1 in s_tmp:
				for s2 in s_tmp2:
					if s2 in interactions3[s1]:
						count_kk_kkk+=interactions3[s1][s2]
			tmp_LRT=tmp_LRT+math.log(B[kk,kkk])*count_kk_kkk  
		count_init_kk=0 #count of interactions initiated from k #assume pi_c are the same across different Ks
		for s1 in s_tmp:
			if s1 in interactions:
				count_init_kk=count_init_kk+len(interactions[s1])
		tmp_LRT=tmp_LRT-math.log(K)*count_init_kk 
	
	if iter>=burn_in:
		for k in range(0,K):
			for s in range(0,N):
				if cluster_ass[s_list[s]]==k:
					clus_out[k][s]+=1
		
		power_law.append([alpha_C,theta_C])
		propensity_matrix.append(B)
		LRT.append(tmp_LRT)

## Output results

if Flag_llk:
	for items in LRT:
		print(items)

if Flag_pl:
	for i in range(len(power_law)):
		print("alpha (iter: "+str(i)+") "+str(power_law[i][0]))
		print("theta (iter: "+str(i)+") "+str(power_law[i][1]))

if Flag_css:
	for items in clus_out:
		print("Block: "+str(items))
		for i in range(len(s_list)):
			print(str(s_list[i])+": "+str(clus_out[items][i]/(iters-burn_in)))

if Flag_B:
	for items in propensity_matrix:
		print(items)

t2=datetime.datetime.now()
print("Running time: "+ str(t2-t1))








