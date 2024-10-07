import numpy as np


def generate_root_distribution():
    """
    Generates a random root distribution until it meets the specified conditions.
    """
    B = False
    while not B:
        R = np.random.dirichlet([1, 1, 1, 1])
        Res = all(ele > 0.2 and ele < 0.3 for ele in R)
        if Res == True:
            B = True
    return R


def rename_nodes(tree):
    """
    Renames the nodes and leaves of the phylogenetic tree.
    """
    for idx, clade in enumerate(tree.get_nonterminals()):
        clade.name = "Node_" + str(idx) if idx > 0 else "Root"
    for idx, clade in enumerate(tree.get_terminals()):
        clade.name = "Leaf_" + clade.name