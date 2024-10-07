import json
import numpy as np
from Bio import Phylo
from io import StringIO

from GenPhylo.utils.misc_utils import generate_root_distribution, rename_nodes
from GenPhylo.utils.matrices_generation import generate_transition_matrices
from GenPhylo.utils.save import save_transition_matrices
from GenPhylo.utils.generate_DNA import generate_alignments

def process_tree(tree, root_distr):
    """
    Process the root distribution and the phylogenetic tree, both user inputs.
    """
    
    if root_distr == "random":
        root_distribution = {"Root": generate_root_distribution()}
    else:
        # Parse a given string separating numbers given by commas and puting them in a 1x4 vector
        root_distribution = np.array(root_distr)
        # Check this vector sums up to 1
        assert sum(root_distribution) == 1, "Root distribution does not sum up to 1"
        root_distribution = {"Root": root_distribution}
    path_t = tree
    tree_file = open(path_t, "r")
    tree = tree_file.read()
    tree = Phylo.read(StringIO(tree), "newick")
    rename_nodes(tree)
    # Write the tree in our format to latter save it at the top of the matrix file
    newick_with_labels = StringIO()
    Phylo.write(tree, newick_with_labels, "newick", format_branch_length='%0.2f')
    newick_with_labels_str = newick_with_labels.getvalue()
    net = Phylo.to_networkx(tree)
    return net, root_distribution, newick_with_labels_str


def get_N_alignments(tree, L, N, root_distr, name):
    """
    Main function to generate transition matrices and alignments.
    """
    
    net, root_distribution, newick_with_labels_str = process_tree(tree, root_distr)
    matrices = generate_transition_matrices(net, root_distribution)
    save_transition_matrices(matrices, name, newick_with_labels_str)
    return generate_alignments(net, root_distribution, matrices, L, N, 1, [], name)


def get_alignments_by_lengths(tree, lengths, root_distr, name):
    """
    Main function to generate transition matrices and alignments.
    """
    
    net, root_distribution, newick_with_labels_str = process_tree(tree, root_distr)
    matrices = generate_transition_matrices(net, root_distribution)
    save_transition_matrices(matrices, name, newick_with_labels_str)
    return generate_alignments(net, root_distribution, matrices, [], [], 2, lengths, name)