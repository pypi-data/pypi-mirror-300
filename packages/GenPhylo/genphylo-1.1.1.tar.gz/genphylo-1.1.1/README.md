# GenPhylo: Generating heterogeneous data on gene trees

### Authors: Marta Casanellas, Martí Cortada, Adrià Diéguez

---

We introduce **GenPhylo**, an open-source Python module for simulating genetic data along a phylogeny avoiding the restriction of continuous-time Markov processes. **GenPhylo** uses directly a general Markov model and therefore naturally incorporates heterogeneity across lineages.

The module has been developed in Python3 and provides an algorithm that can be incorporated in other simulation software.

---

### **Installation and requirements**

Current version of **GenPhylo** is 1.1.1. You can install the package using pip

```diff
pip install GenPhylo
```
**GenPhylo** has several dependencies, please ensure you run

```diff
pip install -r requirements.txt
```
---

### **Using GenPhylo**

Given a tree topology, the branch lengths and the alignment lengths, **GenPhylo** generates GMM parameters and the corresponding alignments, saved in separated output files. The package includes different options for generating the alignments, such as get_N_alignments(), which generates N alignments of fixed length, or get_alignments_by_lengths(), which generates alignments of different lengths.

Below we provide examples of how to use both functions.

**get_N_alignments()**

```python
# Import GenPhylo package
from GenPhylo.utils.alignments_generation import *

tree = 'tree.txt'       # path of your Newick file
L = 1000                # Alignment length
N = 50                  # Number of alignments
root_distr = 'random'   # root distribution (can also be specified by the user, e.g. root_distr = [0.22, 0.24, 0.28, 0.26])
name = 'experiment1'    # output name

# Calling the function that generates the N alignments
get_N_alignments(tree, L, N, root_distr, name)
```
**get_alignments_by_lengths()**

```python
# Import GenPhylo package
from GenPhylo.utils.alignments_generation import *

tree = 'tree.txt'               # path of your Newick file
lengths = [500, 1000, 10000]    # list of alignment lengths
root_distr = 'random'           # root distribution (can also be specified by the user, e.g. root_distr = [0.22, 0.24, 0.28, 0.26])
name = 'experiment2'            # output name

# Calling the function that generates the alignments given the lengths
get_alignments_by_lengths(tree, lengths, root_distr, name)
```
In each case, the outputs (a .txt file with the transition matrices and a .tar with the .FASTA files corresponding to the simulated alignments) are named using the `experiment_name`  parameter and are saved in a directory called `output_files` (if the folder does not already exist, the package will automatically create it).

Additionally, the repository includes an example of the `output_files` directory, as well as an example of the `tree.txt` file for reference. This repository also includes the file `IQ-TREE_analysis.pdf` that describes how we verified the precision of our alignments simulator by using the phylogenetic software **IQ-TREE**.

---

### **CLI implementation**
Within the `cli_app` directory of this repository, we provide a command-line interface (CLI) implementation of the **GenPhylo** package. This allows you to execute **GenPhylo** directly from the terminal without requiring package installation. For detailed instructions on how to run **GenPhylo** via the CLI, please refer to the `README.md` file located in the `cli_app` folder.

---
### **Contributing and Citation**
If you encounter any bugs or have questions, please submit them under the Issues tab at: https://github.com/GenPhyloProject/GenPhylo/issues.

If you use our code, either for your experiments or to develop future research, please cite it:
```
@misc{GenPhylo,
  author       = {Cortada, Martí and Diéguez, Adrià and Casanellas, Marta},
  title        = {{GenPhylo project repository}},
  year         = {2024},
  url          = {https://github.com/GenPhyloProject/GenPhylo},
  note         = {GitHub repository}
}
```
---
### **License**
⚙️ This software is developed under the GNU General Public License v3.
