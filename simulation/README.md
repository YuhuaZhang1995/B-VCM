# Data simulation pipeline

This folder contains the code to generate the simulation data in the paper.

## Description of the Usage

python data_generation.py --output-file test.txt --alpha 0.9 0.1 --theta 5 5 --B 0.9 --K 2 --interc 200 -- pi-prior 10

## Parameters 

- **Required parameter**

`--output-file`: The name of the output file

- **Optional parameter**

`--K`: The number of the underlying communityies. The default value is 2.

`--alpha`: The power-law parameters. The default value is 0.5 for each block.

`--theta`: The power-law parameters. The default value is 5 for each block.

`--B`: The propensity matrix. The default is 0.9 for diagonal values.

`--interc`: The size of the network. The default value is 100 interactions.

`--pi-prior`: The prior of the probaility of an interaction initiating from certain block.
