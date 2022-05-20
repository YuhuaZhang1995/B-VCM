import numpy as np
import math

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

if __name__=="__main__":
	llk(num_vertex,total_deg,k_deg,x)
