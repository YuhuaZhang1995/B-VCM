# Visualization of the results

We show here the code to generate the main results in the paper, which includes: 

**(1) Table 1 and Figure 2: the L2 norm of the block labels and the spaghetti plot**

Use *l2_norm.r* with example data *cluster.txt* and *truth.txt* will generate the L2 norm plot. *cluster.txt* is a file that contains the posterior samples of block assignments from the algorithm and *truth.txt* is a file that contains the ground true block assignments for each node. 

**(2) Figure 3: the spaghetti plot of the model selection**

Figure 3 is the spaghetti plot of the log likelihoods in different models. Use *llk.r* with example data *llk.txt* will calculate the mean llk to generate the spaghetti plot. *llk.txt* contains the posterior samples of the log likelihood.

**(3) Figure 4 and Figure 5(c): degree distribution**

Use *deg_plot.r* with example data *truth.txt* will generate the degree distribution plot.

**(4) Figure 5(a): visualization of adjacency matrix**

Use *figure5a.r* with example data *data1.txt* and *result1.txt* to generate the plot as shown in Figure 5a. *data1.txt* is the ground truth and *result1.txt* is the inferred block assignments.

**(5) Figure 5(b): visualization of the binary matrix**

Use *figure5b.r* with example data *data1.txt*, *data2.txt*, *result1.txt*, and *result2.txt* to generate the plot as shown in Figure 5b. *data1.txt* and *data2.txt* are ground truth from the two parts of the data. *result1.txt* and *result2.txt* are the inferred posterior samples.

**(6) Table 3: Hellinger distance**

Use *table3.r* with example data *data1.txt*, *data2.txt*, *HL1.txt*, and *HL2.txt* to generate the Hellinger distances as shown in Table 3. *data1.txt* and *data2.txt* are ground truth from the two parts of the data. *HL1.txt* and *HL2.txt* are posterior samples.

