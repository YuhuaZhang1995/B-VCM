# Usage

**_Lazy Start with Example data_**

python B-VCM.py --input-file testdata.txt --K 2 --iter 10 --burn-in 5 --output-powerlaw --output-cluster --output-llk --output-


**_Description of the code_**

- **Required parameter**

`--input-file`: Input network data, with each line containing the node1, node2, block assignment of node1, and block assignment of node2
, separated by tab. **_e.g. --input-file testdata.txt**

- **Optional parameter**

`--K`: The presumed number of underlying communities. The user can use **_python B-VCM.py --input-file testdata.txt --K 2_** to specify the number of blocks. The default value if K=2.

`--iter`: The number of total iteractions in Gibbs Sampling algorithm. The user can use **_python B-VCM.py --input-file testdata.txt --iter 1000_** to specify the number of iterations. Default is 2000.

`--burn-in`: The number of burn-in's in Gibbs Sampling algorithm. It needs to be smaller than the total number of iteractions. The user can use **_python B-VCM.py --input-file testdata.txt --burn-in 500_** to specify the number of burn-in's. Default is 1000.

- **Output results**

`--output-powerlaw`: With this option, the user can output power-law parameters from the algorithm.

`--output-cluster`: With this option, the user can output the block assignments of each node. The output is a probability, representing the times a node is assigned to a certain block over the iteractions.

`--output-llk`: With this option, the user can output marginal log likelihood of the model.

`--output-propensity`: With this option, the user can output the propensity of within/between block connection.

