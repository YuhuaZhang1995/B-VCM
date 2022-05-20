import numpy as np

"""We have 3 parameters in updating the e2 llk: total deg(a scalar for each block), num_vertex(a scalar for each block), count_tmp(a dict), count_KK(scalar)"""
# (1) total_deg={1:tot_deg,2:tot_deg,...,K:tot_deg}
# (2) num_vertex={1:num_vex, 2:num_vex,...,K:num_vex}
# (3) count={1:{deg1:#,deg2:#,...,degN:#},2:{deg1:#,deg2:#,...,degN:#},...,K:{deg1:#,deg2:#,...,degN:#}}
# (4) count_KK={1:init#, 2:init#,...,K:init#}

def degree_count(total_deg_K, num_vertex_K, count_K, count_KK,cluster_ass, interactions, count_all,K):
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

if __name__=="__main__":
	degree_count(total_deg_K, num_vertex_K, count_K, count_KK, cluster_ass, interactions,K)
