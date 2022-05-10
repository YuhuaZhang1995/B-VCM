import numpy as np
import math
import scipy.optimize as opt
from scipy.optimize import minimize
import sys

def llk(num_vertex,total_deg,k_deg,x):
	"""k_deg=a disctionary with key=degree, value=count of vertex"""
	"""num_vertex= number of vertex"""
	"""total_degree=total degree, 2*nrow"""
	"""x=[alpha,theta]"""
	alpha=x[0]
	theta=x[1]
	keys=np.array(list(dict.keys(k_deg)))
	values=np.array(list(dict.values(k_deg)))
	tmp=np.array(list(map(math.lgamma,(keys-alpha))))-math.lgamma(1-alpha)
	llk_=num_vertex*math.log(alpha)+math.lgamma(theta/alpha+num_vertex)-math.lgamma(theta/alpha)-math.lgamma(theta+total_deg)+math.lgamma(theta)+sum(np.multiply(values,tmp))
	return 0-llk_

## Input file processing
## count the number of senders
remove_header=0
obs=[]
count_all={}
cluster_ass={}
interactions={} #for add-on
interactions2={} #for add-on
interactions3={}
interactions4={}
filename=sys.argv[1]
with open(filename) as infile:
	for line in infile:
		remove_header=remove_header+1
		s1=line.strip().split("\t")[0]
		s2=line.strip().split("\t")[1]
		cs1=line.strip().split("\t")[2]
		cs2=line.strip().split("\t")[3]
		#if change the sender, restart the loop
		if remove_header>1:
			#if int(s1) !=int(s2):
			obs.append([int(s1),int(s2)])
			if not int(s1) in count_all:
				count_all[int(s1)]=1
			else:
				count_all[int(s1)]+=1

			if not int(s2) in count_all:
				count_all[int(s2)]=1
			else:
				count_all[int(s2)]+=1
				
			if not int(s1) in cluster_ass:
				cluster_ass[int(s1)]=int(cs1)
			if not int(s2) in cluster_ass:
				cluster_ass[int(s2)]=int(cs2)
			if not int(s1) in interactions:
				interactions[int(s1)]=[int(s2)]
			else:
				interactions[int(s1)].append(int(s2))
			if not int(s2) in interactions2:
				interactions2[int(s2)]=[int(s1)]
			else:
				interactions2[int(s2)].append(int(s1))
			
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

# Given value of alpha_zero and K
K=int(sys.argv[2])
alpha_zero=[1]*K
a=[1]*K
b=[1]*K
c=[1]*K
d=[1]*K
Bb=np.ones((K,K))

# Initialize B, alpha_C, theta_C
B=np.ones((K,K))/K
alpha_C=np.ones(K)/2
theta_C=np.ones(K)*10

# Initialize C_s
N=len(count_all)
s_list=list(count_all.keys())
s_list.sort()

cluster_ass={}
for i in range(0,N):
	cluster_ass[s_list[i]]=np.where(np.random.multinomial(1,[0.5,0.5])==1)[0][0]

#Gibbs sampling

###We have 3 parameters in updating the e2 llk: total deg(a scalar), num_vertex(a scalar), count_tmp(a dict), count_KK(scalar)
# to rerwite the code for K>2, need:
# (1) total_deg={1:tot_deg,2:tot_deg,...,K:tot_deg}
# (2) num_vertex={1:num_vex, 2:num_vex,...,K:num_vex}
# (3) count={1:{deg1:#,deg2:#,...,degN:#},2:{deg1:#,deg2:#,...,degN:#},...,K:{deg1:#,deg2:#,...,degN:#}}
# (4) count_KK={1:init#, 2:init#,...,K:init#}

total_deg_K={}
num_vertex_K={}
count_K={}
count_KK={}

for k in range(0,K):
	s_tmp=np.array([key for key, value in cluster_ass.items() if value == k])
	num_vertex=len(s_tmp)
	num_vertex_K[k]=num_vertex
	count_tmp= {tt: count_all[tt] for tt in s_tmp if tt in count_all}
	total_deg=list(count_tmp.values())
	total_deg=sum(total_deg)
	count={}
	for i in count_tmp.keys():
		if count_tmp[i] in count.keys():
			count[count_tmp[i]]+=1
		else:
			count[count_tmp[i]]=1
	total_deg_K[k]=total_deg
	count_K[k]=count
	count11=0 #Count of interactions initialed from s1 in cluster k
	for s1 in s_tmp:
		if s1 in interactions:
			count11=count11+len(interactions[s1])
	count_KK[k]=count11
#print(count_K[0])

clus_out={}
for k in range(0,K):
	clus_out[k]=np.zeros(len(s_list))
LRT=[]
for iter in range(0,2000):
	#print([alpha_C,theta_C])
	#print(B)
	#print(np.linalg.norm(C_s-C_s_ass))
	#print(cluster_ass)	
	
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


		#print(tmp_p)
		###sample cluster assignment
		if (np.unique(tmp_p)[-1]-np.unique(tmp_p)[-2])>30:
			new_ass=np.where(tmp_p==max(tmp_p))[0][0]
		else:
			tmp_p=np.array(tmp_p)-max(tmp_p)
			for kk in range(0,K):
				tmp_p[kk]=math.exp(tmp_p[kk])
			tmp_p=np.array(tmp_p)/sum(np.array(tmp_p))
			new_ass=np.where(np.random.multinomial(1,tmp_p)==1)[0][0]
		
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

	if iter>999:
		for k in range(0,K):
			for s in range(0,N):
				if cluster_ass[s_list[s]]==k:
					clus_out[k][s]+=1

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
				#if count_all[mm[0]]!=1 and count_all[mm[1]]!=1:
				if cluster_ass[mm[0]]==i:
					count1+=1
					if cluster_ass[mm[1]]==j:
						count2+=1
			tmp_alpha.append(count2)
      B[i,:]=np.random.dirichlet(tmp_alpha+np.array(Bb[i,:])[0],1)[0]

