import numpy as np
import math
import scipy.optimize as opt
import sys
from collections import defaultdict

#################Simulation scheme####################
#1. Sample the cluster assignment based on the Dirichlet-Multinomial Distribution for only sender 1
#2. Sample the sender 1 based on the cluster assignment and the pre-specified model parameters $\{\alpha_{C_s},\theta_{C_s}\}$
#3. Decide whether within cluster interactions or between cluster interactions given the matrix B. 
#4. Once decided the clustering assignment of sender 2, sample the sender 2 from the corresponding cluster assignment pool.
#5. Repeat the whole procedure until the desired number of interactions are sampled


def gen_sample(alpha,theta,alpha_zero,B,interactions,generated_int,iter):
	for i in range(0,iter):
		#Cluster assignment of sender 1
		pi_s=np.random.dirichlet(alpha_zero)
		pi_s=[0.5,0.5]
		C_s1=np.random.multinomial(1,pi_s)
		C_s1=np.where(C_s1==1)[0][0]
		
		#generate the sender 1 based on the cluster assignment
		
		#The first obs
		if len(interactions[C_s1])==0:
			s1=0
			interactions[C_s1].append(1)
		#If not the first obs
		else:
			p=(np.array(interactions[C_s1])-alpha[C_s1])/(sum(interactions[C_s1])+theta[C_s1]) #sample an observed sender
			p=np.append(p,1-sum(p)) #append the prob of observing a new sender
			#print(p)
			s1=np.random.multinomial(1,p)
			s1=np.where(s1==1)[0][0]
		
			#If sender 1 is new
			if len(interactions[C_s1])==s1:
				interactions[C_s1].append(1)
			#If sender 1 has been observed
			else:
				interactions[C_s1][s1]+=1
	
		#Given the cluster and the sender, decide which cluster to sample sender 2
		C_s2=np.random.multinomial(1,np.array(B[:,C_s1]))
		C_s2=np.where(C_s2==1)[0][0]
	
		#Once decided the cluster assignment for sender 2, sample sender 2
		if len(interactions[C_s2])==0:
			s2=0
			interactions[C_s2].append(1)

		else:
			p=(np.array(interactions[C_s2])-alpha[C_s2])/(sum(interactions[C_s2])+theta[C_s2]) #sample an observed one
			p=np.append(p,1-sum(p))
			#print(p)
			s2=np.random.multinomial(1,p)
			s2=np.where(s2==1)[0][0]
		
			#If sender 2 is new
			if len(interactions[C_s2])==s2:
				interactions[C_s2].append(1)
			#If sender 2 has been observed
			else:
				interactions[C_s2][s2]+=1
		#labeling the sender 1 and sender 2 according to corresponding cluster
		#Assume the senders doesn't overlap across different clusters
		generated_int.append([K*s1+C_s1,K*s2+C_s2,C_s1,C_s2])
	return(generated_int)

###########Initialization########
K=2
alpha_zero=[10]*K
alpha=[0.5]*K
theta=[5]*K
B=np.ones((K,K))/(1/0.1*(K-1))
np.fill_diagonal(B, 0.9)
size=100


command=sys.argv[1:]
for i in range(len(command)):
	if command[i]=="--alpha":
		for k in range(K):
			alpha[k]=float(command[i+1+k])
	if command[i]=="--theta":
		for k in range(K):
			theta[k]=float(command[i+1+k])
	if command[i]=="--B":
		B=np.ones((K,K))/(1/(1-float(command[i+1]))*(K-1))
		np.fill_diagonal(B, float(command[i+1]))
	if command[i]=="--prior-pi":
		alpha_zero=[float(command[i+1])]*K
	if command[i]=="--K":
		K=int(command[i+1])
	if command[i]=="--interc":
		size=int(command[i+1])
	if command[i]=="--output-file":
		filename=command[i+1]

listKeys=list(range(0,K))
interactions=defaultdict(list)
for i in listKeys:
    interactions[i]=[]

generated_int=[]
##########Generate the data###########
gen_sample(alpha,theta,alpha_zero,B,interactions,generated_int,size)

#######Write the data to files##########
with open(filename,"a") as myfile:
	tmp="node1\tnode2\tc1\tc2\n"
	myfile.write(tmp)
	for i in generated_int:
		sender=i[0]
		receiver=i[1]
		tmp=str(sender)+"\t"+str(receiver)+"\t"+str(i[2])+"\t"+str(i[3])+"\n"
		myfile.write(tmp)
myfile.close()
