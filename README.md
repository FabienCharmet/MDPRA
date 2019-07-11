### Markov Decision Process for Resource Allocation

Welcome to the MDPRA project.
This project generates the MDP states, transition and reward matrixes for the secure migration.

## Prerequisite

PLEASE NOTE THAT THIS TOOL IS INTENDED TO WORK FOR LINUX !
Implementation for PowerShell on Windows is ongoing.

The installation procedure of the MDP toolbox can be found here:

[https://pymdptoolbox.readthedocs.io/en/latest/index.html] (https://pymdptoolbox.readthedocs.io/en/latest/index.html)

## Installing

```
git clone https://github.com/FabienCharmet/MDPRA

```
Or simply download the source code

## Usage

### Generatin the MDP files


```
python genmodel.py <topology size> <bf budget> <bc budget> <migration size> <generation mode> <topology file> <detection probability>
```

1. \<topology size\> : Number of nodes in the infrastructure
2. \<bf budget\> : Financial budget
3. \<bc budget\> : Computational budget
4. \<migration size\> : Number of nodes to be migrated (Size of the Virtual Network)
5. \<generation mode\> : Type of algorithm used to generate the MDP (available mode: normal)
6. \<topology file\> : Description of the physical infrastructureo
7. \<detection probability\> : Probability of one monitoring node to detect an attack coming through

PLEASE NOTE THAT \<topology size\> must match the number of nodes in \<topology file\>
For example, if \<topology size\> == 6 then use topo6 or topo6m topology files.

### Topology file

source[0] is the location of the extraction point. source[i] is the source location of the attack on node i
node_migr is the index of the nodes that will embed the Virtual Network
```
source = [6,6,6,6,6,6,6] #loc://github.com/FabienCharmet/MDPRAtion of the attacker
node_migr=[1,2,3]

graph = { "1" : ["2","3","4"],
    "2" : ["1","4"],
    "3" : ["1","4","5"],
    "4" : ["1","2","3","6"],
    "5" : ["3","6"],
    "6" : ["4","5"]
}

dij = Graph(graph)

```

This will generate several files including:  

- model_log-XXX : Raw file
- model-XXX : Sorted file without duplicate lines
- counter-XXX : Used to determine number of reccursive calls
- generation_time : Generation log and duration



### Extracting the optimal policy

```
python viextracttion.py <model-file> <topology size> check
```

check option is used to verify transition matrixes and make them stochastic

Generate several files:

- states_name-XXX : Equivalence between numbered states and states from log file
- mdp-results-XXX : Stores optimal policy, rewards etc.

## Automated result generation 
1. result_generation.py : Loops to generate several MDP files
2. mdp_extraction.py : Loops to determine the optimal policy of all generated files
3. result_extraction.py : Generates laTeX code for result exploitation

Generated files:
statefile: LaTeX diagram for individual node importance
globalresults-model-XXX : Provides individual results 
policy-XXXX : List states in the optimal policy and the associated optimal action
mdptable-XXX : Individual results for specific probability
tablefile : Global results of the extraction 

Files must be used in that order to generate appropriate files.
Please note that they are currently set on the same parameters to be a working example.
Changes must be made to adapt to your desired parameters.


## Important notes

Some parameters are hardcoded, such as attack probability, nodes values and migration size for automated result generation.
For use case reproduction, please use provided files.
Automated result generation can use parallelization to reduce generation and computation time.
This may slow your computer.
Parallelization can be activatin by uncommenting the subprocess line and changing os.system line accordingly
However, it is highly recommended to limit the number of simultaneous subprocess calls.

## Debugging tools
showgraph.py is used to represent a graph of the connected states in the optimal policy.
He uses numpy.loadtxt to load the transition matrix of the optimal policy and verify what which states are connected together.
In order to be used, specific installation is required using python3 and networkX.
Moreover, in order to use showgraph.py viextraction.py must be modified to use numpy.savetxt on the transition matrix you want to observe.
Please note that the labelling process only matches the states names if using P1 as defined in viextraction.py.
Labelling process will be adapted in the future.
