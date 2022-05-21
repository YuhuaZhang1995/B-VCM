# Community Detection within Edge Exchangeable Model for Interaction Processes

Scientists are increasingly interested in discovering community structure from modern relational data arising on large-scale social networks. While many methods have been proposed for learning community structure, few account for the fact that these modern networks arise from processes of interactions in the population. We introduce block edge exchangeable models (BEEM) for the study of interaction networks with latent node-level community structure. The block vertex components model (B-VCM) is derived as a canonical example. Several theoretical and practical advantages over traditional vertex-centric approaches are highlighted. In particular, BEEMs allow for sparse degree structure and power-law degree distributions within communities. Our theoretical analysis bounds the misspecification rate of block assignments,
while supporting simulations show the properties of the network can be recovered. A computationally tractable Gibbs algorithm is derived. We demonstrate the proposed model using post-comment interaction data from Talklife, a large-scale online peer-to-peer support network.

## Project Description

The Project includes the code needed to reproduce results, which includes

(1) The implementation of B-VCM model (See details at [B-VCM](https://github.com/YuhuaZhang1995/B-VCM/blob/main/B-VCM/README.md))

(2) The simulation pipeline used to generate the data (See details at [Simulation](https://github.com/YuhuaZhang1995/B-VCM/blob/main/README.md))

(3) The visualization of the results (See details at [Plots](https://github.com/YuhuaZhang1995/B-VCM/blob/main/visualization/README.md))

(4) The code to generate the comparison results with other methods (See details at [Other methods](https://github.com/YuhuaZhang1995/B-VCM/blob/main/Comparison%20In%20TalkLife/README.md))


